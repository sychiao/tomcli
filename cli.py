import click
import toml
import subprocess
from string import Template

def buildOption(name, df_, ty_):
    return click.option(f"--{name}", default=df_, type=ty_, show_default=True)

def buildOptions(dct):
    lst = list()
    for name, value in dct.items():
       if isinstance(value, dict):
           op = buildOption(name, list(value)[0], click.Choice(list(value)))
       elif isinstance(value, bool|int|str):
           op = buildOption(name, value, type(value))
       lst.append(op)
    return lst

def ParseToml(conf):
    cmds = conf["commands"]
    global_option = dict()
    cmds_option = {cmd: None for cmd in cmds}
    for options, value in conf.items():
        if options != "commands" and options not in cmds:
            global_option[options] = value
        if options in cmds:
            cmds_option[options] = value
    return cmds, global_option, cmds_option

def BuildCommand(line, options):
    @click.command(help=line)
    @click.pass_context
    def shell(ctx, *args, **kwargs):
        dct = ctx.obj | kwargs
        command = Template(line).substitute(dct)
        print("Execute ==>> ", command)
        subprocess.run(command, shell=True)

    if options:
      for f in buildOptions(options):
        shell = f(shell)

    return shell

def ConstructCLI(cmds, global_option, cmds_option):
  @click.group()
  @click.pass_context
  def cli(ctx, *args, **kwargs):
      ctx.obj = kwargs

  for func in buildOptions(global_option):
      cli = func(cli)

  for cmd_name, cmdline in cmds.items():
      cli.add_command(BuildCommand(cmdline, cmds_option[cmd_name]), cmd_name)
  return cli

import sys

def main():
  conf = toml.load(sys.argv[1])
  sys.argv = sys.argv[1:]
  ConstructCLI(*ParseToml(conf))(obj={})

main()

# cli(obj={})

