# -*- coding: utf-8 -*-
'''
Module to provide access to Mattermost Command Line Tools (platform)
'''

import salt
import salt.utils

from salt.exceptions import (
    CommandExecutionError
)

import logging

log = logging.getLogger(__name__)

__virtualname__ = 'mattermost'


def __virtual__():
    '''
    Return virtual name of the module.
    :return: The virtual name of the module.
    '''
    
    return __virtualname__


def _get_path():
    '''
    Returns Mattermost installation path
    '''
    
    return __grains__['mattermost_path']


def _get_cmd():
    '''
    Returns Mattermost platform command path
    '''
    return _get_path() + '/bin/platform'


def _get_cfg():
    '''
    Returns Mattermost platform default configuration file path
    '''
    
    return _get_path() + '/config/config.json'


def _get_options(command=None, **kwargs):
    '''

    :param config:
    :param username: Username used in other commands
    :param email: Email address used in other commands
    :param password:
    :param team_name: The team name used in other commands
    :param role:
    :return:
    '''
    if command is None:
        return []

    options = [command]
    config = kwargs.get('config')
    username = kwargs.get('username')
    email = kwargs.get('email')
    password = kwargs.get('password')
    team_name = kwargs.get('team_name')
    role = kwargs.get('role')
    site_url = kwargs.get('site_url')
    channel_name = kwargs.get('channel_name')
    license_path = kwargs.get('license_path')

    if config:
        options += ['-config=' + config]
    else:
        options += ['-config=' + _get_cfg()]
    if username:
        options += ['-username=' + username]
    if email:
        options += ['-email=' + email]
    if password:
        options += ['-password=' + password]
    if team_name:
        options += ['-team_name=' + team_name]
    if role:
        options += ['-role=' + role]
    if site_url:
        options += ['-site_url=' + site_url]
    if channel_name:
        options += ['-channel_name=' + channel_name]
    if license_path:
        options += ['-license_path=' + license_path]

    return options


def _platform_run(command):
    return __salt__['cmd.run_all'](command, cwd=_get_path(), python_shell=False)


def create_team(team_name,
                email):
    '''
    Creates a team.

    :param team_name:
    :param email:
    :return:

    Example:

    salt '*' mattermost.create_team team_name="name" email="user@example.com"

    '''

    command = [_get_cmd()] + _get_options(command='-create_team', team_name=team_name, email=email)
    result = _platform_run(command)

    # if result['retcode'] != 0:
    #     log.error(
    #         'dig returned exit code \'{0}\'.'.format(
    #             cmd['retcode']
    #         )
    #     )

    if result['retcode'] != 0:
        log.error('platform returned exit code \'{0}\'.'.format(result['retcode']))
        # log.error(result['stdout'])
        # log.error(result['stderr'])
        raise CommandExecutionError('Could not create team.')
    else:
        return True


def create_user(username, password, team_name, email, config=None):
    '''
    Creates a user.

    :param team_name: Team name.
    :param email: Email.
    :return:

    Example:

    salt '*' mattermost.create_team team_name="name" email="user@example.com"

    '''
    command = [_get_cmd()] + _get_options(command='-create_user',
                                          username=username,
                                          password=password,
                                          team_name=team_name,
                                          email=email,
                                          config=config)
    result = _platform_run(command)
    if result['retcode'] != 0:
        log.error('platform returned exit code \'{0}\'.'.format(result['retcode']))
        # log.error(result['stdout'])
        # log.error(result['stderr'])
        raise CommandExecutionError('Could not create user.')

        # for key in ('stderr', 'stdout'):
        #     if result[key]:
        #         for line in result['stdout'].splitlines():
        #             if "Couldn\'t save the user" in line:
        #                 raise CommandExecutionError("save the user")


def invite_user(team_name, email, site_url):
    '''
    Invites a user to a team by email.

    :param team_name:
    :param email:
    :return:

    Example:

    salt '*' mattermost.create_team team_name="name" email="user@example.com"

    '''
    
    command = [_get_cmd()] + _get_options(command='-invite_user', team_name=team_name, email=email, site_url=site_url)
    result = _platform_run(command)
    if result['retcode'] != 0:
        log.error('platform returned exit code \'{0}\'.'.format(result['retcode']))
        # log.error(result['stdout'])
        # log.error(result['stderr'])
        raise CommandExecutionError('Could not invite user.')
    else:
        return True


def join_team(email, team_name):
    '''
    Invites a user to join a team by email.

    :param team_name:
    :param email:
    :return:

    Example:

    salt '*' mattermost.create_team team_name="name" email="user@example.com"

    '''
    command = [_get_cmd()] + _get_options(command='-join_team', email=email, team_name=team_name)
    result = _platform_run(command)

    if result['retcode'] != 0:
        log.error('platform returned exit code \'{0}\'.'.format(result['retcode']))
        # log.error(result['stdout'])
        # log.error(result['stderr'])
        raise CommandExecutionError('Could not invite user to join team.')


def assign_role(email, role):
    '''
    Invites a user to join a team by email.

    :param team_name:
    :param email:
    :return:

    Example:

    salt '*' mattermost.create_team team_name="name" email="user@example.com"

    '''
    command = [_get_cmd()] + _get_options(command='-assign_role', email=email, role=role)
    result = _platform_run(command)
    if result['retcode'] != 0:
        log.error('platform returned exit code \'{0}\'.'.format(result['retcode']))
        # log.error(result['stdout'])
        # log.error(result['stderr'])
        raise CommandExecutionError('Could not create user.')


def join_channel(email, team_name, channel_name, license=None):
    '''
    Invites a user to join a team by email.

    :param team_name:
    :param email:
    :return:

    Example:

    salt '*' mattermost.create_team team_name="name" email="user@example.com"

    '''
    command = [_get_cmd()] + _get_options(command='-join_channel', email=email, team_name=team_name,
                                          channel_name=channel_name)
    result = _platform_run(command)
    for key in ('stderr', 'stdout'):
        if result[key]:
            for line in result['stderr'].splitlines():
                if "Feature requires an enterprise license" in line:
                    raise CommandExecutionError("Feature requires an enterprise license")

    if result['retcode'] != 0:
        log.error('platform returned exit code \'{0}\'.'.format(result['retcode']))
        for key in ('stderr', 'stdout'):
            if result[key]:
                for line in result['stderr'].splitlines():
                    if "Feature requires an enterprise license" in line:
                        raise CommandExecutionError("Feature requires an enterprise license")
    raise CommandExecutionError('Could not create user.')


def leave_channel():
    return 0


def list_channels():
    comando = ['/home/vagrant/mattermost/bin/platform', '--config=/home/vagrant/mattermost/config/config.json',
               '-list_channels']
    cmd = __salt__['cmd.run'](comando, cwd='/home/vagrant/mattermost', python_shell=False)
    return cmd['stdout'].split('\n')


def restore_channel():
    return 0


def reset_password(email, password):
    command = [_get_cmd()] + _get_options(command='-reset_password', email=email, password=password)
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def reset_mfa(username):
    command = [_get_cmd()] + _get_options(command='-reset_mfa', username=username)
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def reset_database():
    command = [_get_cmd()] + _get_options(command='-reset_database')
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def permanent_delete_user(email):
    command = [_get_cmd()] + _get_options(command='-permanent_delete_user', email=email)
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def permanent_delete_all_users(team_name,
                               email
                               ):
    command = [_get_cmd()] + _get_options(command='-permanent_delete_all_users')
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def permanent_delete_team(team_name):
    command = [_get_cmd()] + _get_options(command='-upload_license')
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def upload_license(license_path):
    command = [_get_cmd()] + _get_options(command='-reset_database')
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def upgrade_db_30():
    command = [_get_cmd()] + _get_options(command='-upgrade_db_30')
    result = _platform_run(command)
    if result['retcode'] > 0:
        return result['stderr']
    return result['stdout']


def version():
    command = [_get_cmd()] + _get_options(command='-version')
    result = _platform_run(command)
    return result
