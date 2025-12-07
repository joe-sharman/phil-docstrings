import glob
import logging

import click

from .model import GeminiModel
from .parser import DocstringInserter
from .prompt import PromptBuilder


logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--source-dir",
    "-s",
)
@click.option(
    "--target-dir",
    "-t",
)
@click.option(
    "--token"
    , envvar="GOOGLE_API_KEY"
)
@click.option("--include-description", "-d", is_flag=True, default=True)
@click.option("--include-args", "-i", is_flag=True, default=False)
@click.option("--include-return-types", "-r", is_flag=True, default=False)
@click.option("--include-exceptions", "-e", is_flag=True, default=False)
@click.option("--include-example-usage", "-u", is_flag=True, default=False)
def run(
    source_dir: str,
    target_dir: str,
    token: str,
    include_description: bool,
    include_args: bool,
    include_return_types: bool,
    include_exceptions: bool,
    include_example_usage: bool,
):
    prompt_builder = PromptBuilder(
        include_description,
        include_args,
        include_return_types,
        include_exceptions,
        include_example_usage,
    )
    model = GeminiModel(token)

    for filename in glob.iglob("**/*.py", recursive=True, root_dir=source_dir):
        logger.info(f"Processing file {filename}")
        DocstringInserter(
            f"{source_dir}/{filename}", f"{target_dir}/{filename}", model, prompt_builder
        ).run()
