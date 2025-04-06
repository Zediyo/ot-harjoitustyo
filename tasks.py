from invoke import task
from subprocess import call
from sys import platform

def is_windows():
	return platform == "win32"
	
@task
def start(ctx):
	if is_windows():
		ctx.run("python src/index.py", pty=False)
	else:
		ctx.run("python3 src/index.py", pty=(platform != "win32"))

@task()
def test(ctx):
	ctx.run("pytest src", pty=(platform != "win32"))

@task
def coverage(ctx):
	ctx.run("coverage run --branch -m pytest src", pty=(platform != "win32"))

@task(coverage)
def coverage_report(ctx):
	ctx.run("coverage html", pty=(platform != "win32"))
	if platform != "win32":
		call(("xdg-open", "htmlcov/index.html"))
	else:
		call(("start", "htmlcov/index.html"), shell=True)

@task
def lint(ctx):
	ctx.run("pylint src", pty=(platform != "win32"))

@task
def format(ctx):
	ctx.run("autopep8 --in-place --recursive src", pty=(platform != "win32"))