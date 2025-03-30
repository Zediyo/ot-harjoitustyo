from invoke import task
from subprocess import call
from sys import platform

@task
def foo(ctx):
	print("bar")
	
@task
def start(ctx):
	ctx.run("python3 src/index.py", pty=True)

@task()
def test(ctx):
	ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
	ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
	ctx.run("coverage html", pty=True)
	if platform != "win32":
		call(("xdg-open", "htmlcov/index.html"))
		
@task
def startw(ctx):
	ctx.run("python src/index.py")

@task()
def testw(ctx):
	ctx.run("pytest src")

@task
def coveragew(ctx):
	ctx.run("coverage run --branch -m pytest src")

@task(coveragew)
def coverage_reportw(ctx):
	ctx.run("coverage html")
	if platform != "win32":
		call(("xdg-open", "htmlcov/index.html"))