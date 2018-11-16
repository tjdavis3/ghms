import click
from github import Github
from github.GithubException import UnknownObjectException
import os
from jinja2 import Environment, FileSystemLoader

dirname = os.path.dirname(os.path.abspath(__file__))

GITHUB_REPOS = ( 'teliax/ivy',
                 'teliax/ivy-issues',
                 'teliax/bonsai',
                 'teliax/tax-code-service' )

class Config(object):
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repos = GITHUB_REPOS

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--token', help='GitHub access token')
#@click.argument('repos', nargs=-1)
@pass_config
def cli(config, token):
    """
    Manipulates milestones on several github repositories at once.
    """
    if token and len(token) > 0:
        config.github_token = token
    #if repos:
    #    config.github_repos = repos

@click.command()
@click.argument('old_title')
@click.argument('new_title')
@pass_config
def rename(config, old_title, new_title):
    """ Rename a milestone """
    exec_github(config.github_token, config.github_repos, 'rename', old_title, new_title=new_title)

@click.command()
@click.argument('title')
@pass_config
def delete(config, title):
    """ Delete the given milstone """
    exec_github(config.github_token, config.github_repos, 'delete', title)

@click.command()
@click.argument('title')
@click.option('--description', help="Description of the milestone")
@pass_config
def create(config, title, description=''):
    "Create a new milestone in all repositories"
    if description is None:
        description = ''
    exec_github(config.github_token, config.github_repos, 'create', title, description=description)

@click.command()
@click.argument('title')
@pass_config
def close(config, title):
    """ Close the given milestone """
    exec_github(config.github_token, config.github_repos, 'close', title)

@click.command()
@click.argument('title')
@click.option('--detail/--no-detail', default=False)
@click.option('--label', help="Only report issues with this label")
@pass_config
def report(config, title, detail, label=None):
    milestone_report(config.github_token, config.github_repos, title, verbose=detail, label=label)

def exec_github(token, repos, command, title, description='', new_title=''):
    gh = Github(token)

    for repo in repos:
        r = gh.get_repo(repo)
        if command == 'create':
            r.create_milestone(title=title, description=description)
        else:
            milestones = r.get_milestones()
            for milestone in milestones:
                if milestone.title == title:
                    if command == 'delete':
                        milestone.delete()
                    elif command == 'rename':
                        milestone.edit(title=new_title)
                    elif command == 'close':
                        milestone.edit(title, state='closed')

def milestone_report(token, repos, title, verbose=False, label=None):
    gh = Github(token)
    first_milestone = None
    issues = {}

    for repo in repos:
        r = gh.get_repo(repo)
        milestones = r.get_milestones()
        label_obj = ""
        if label:
            try:
                l = r.get_label(label)
                label_obj = [l]
            except UnknownObjectException:
                continue
        for milestone in milestones:
            if milestone.title == title:
                if not first_milestone:
                    first_milestone = milestone
                github_issues = r.get_issues(milestone=milestone, state='all', labels=label_obj)
                if github_issues.totalCount > 0:
                    issues[r] = github_issues
    env = Environment()
    loader = FileSystemLoader(dirname)
    tmpl  = loader.load(env, 'milestone.md')
    context=dict(issues=issues, milestone=first_milestone, verbose=verbose)
    print tmpl.render(context)

cli.add_command(rename)
cli.add_command(delete)
cli.add_command(create)
cli.add_command(close)
cli.add_command(report)

if __name__ == '__main__':
    cli()
