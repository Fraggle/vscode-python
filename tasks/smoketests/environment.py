# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import sys

from tasks.smoketests.setup import (
    clear_code,
    setup_user_settings,
    setup_workspace,
    start_application,
)
from tasks.smoketests.utils.tools import empty_directory
from tasks.smoketests.vscode.application import get_options
from tasks.smoketests.vscode.base import Context
from tasks.smoketests.vscode.extension import load_python_extension


def before_all(context: Context):
    context.options = options = get_options(**context.config.userdata)
    empty_directory(context.options.workspace_folder)
    settings = {"python.pythonPath": sys.executable}
    setup_user_settings(options.user_dir, user_settings=settings)
    context.app = start_application(options)
    load_python_extension(context.app)


def after_all(context: Context):
    context.app.exit()


def before_feature(context: Context, feature):
    repo = [tag for tag in feature.tags if tag.startswith("https://")]
    empty_directory(context.options.workspace_folder)
    if len(repo) == 1:
        setup_workspace(
            repo[0], context.options.workspace_folder, context.options.temp_folder
        )


def before_scenario(context: Context, feature):
    context.options = get_options(**context.config.userdata)
    empty_directory(context.options.workspace_folder)
    clear_code(context.app)


def after_scenario(context: Context, feature):
    context.app.notifications.clear()
