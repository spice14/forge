import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """Say hello to someone."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    print("[debug] CLI entrypoint reached")
    app()
