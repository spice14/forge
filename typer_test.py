import typer

app = typer.Typer()

def main(name: str = typer.Option(..., "--name", help="Name to greet")):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    print("[debug] CLI entrypoint reached")
    typer.run(main)
