from ontogen.service import app

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5002

    import sys

    for arg in sys.argv:
        if "=" in arg:
            k = arg.split("=")[0]
            v = arg.split("=")[1]

            if k == "host":
                host = v
            if k == "port":
                port = int(v)

    # Run the OntoGen service
    app.run(host=host, port=port, debug=True)
