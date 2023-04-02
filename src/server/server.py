from psutil import sensors_battery
from flask import Flask, request, jsonify


def create_app(stats_queue, get_interval, post_interval, shutdown_delay):
    app = Flask(__name__)

    @app.route("/config", methods=["GET"])
    def config():
        """
        Used by the client to sync configuration.
        """
        return jsonify({
            "get_interval": get_interval,
            "post_interval": post_interval,
            "shutdown_delay": shutdown_delay,
        })

    @app.route("/get_battery", methods=["GET"])
    def get_battery():
        """
        The only possible scenario where the client will interpret "no power outage" is when the server returns 1,
        all other cases (including a failed request in case the server is down) will signal a power outage. I decided on
        this behaviour because a false-positive is preferable to the scenario where there is an actual outage and the
        server is down so the client burns through the entire UPS backup (causing additional wear and tear).
        """
        battery = sensors_battery()
        if battery is not None:
            return "1" if battery.power_plugged else "0"
        else:
            return "battery not found", 404  # lol

    @app.route("/post_stats", methods=["POST"])
    def post_stats():
        """
        Client will post statistic to this endpoint.
        """
        stats_queue.put(request.json)
        return "ok", 200

    return app


if __name__ == "__main__":
    from queue import Queue
    from defaults import *

    create_app(
        Queue(),
        GET_INTERVAL,
        POST_INTERVAL,
        SHUTDOWN_DELAY
    ).run(
        HOST, PORT, debug=False
    )
