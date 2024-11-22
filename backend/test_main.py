import pytest
from click.testing import CliRunner
from main import cli


@pytest.fixture
def runner():
    return CliRunner()


# test ETL
def test_extract_transform_load(runner):
    result = runner.invoke(cli, ["extract-transform-load"])
    assert result.exit_code == 0, result.exit_code
    # assert "Data extracted, transformed, and loaded successfully." in result.output
    print(result.output)


# test CRUD operations
def test_create(runner):
    result = runner.invoke(
        cli,
        [
            "create",
            "101",
            "otro",
            "175",
            "12333",
            "blonde",
            "green",
            "blue",
            "male",
            "2",
        ],
    )
    assert result.exit_code == 0
    print(result.output)


def test_read(runner):
    result = runner.invoke(cli, ["read"])
    assert result.exit_code == 0
    print(result.output)


def test_update(runner):
    result = runner.invoke(
        cli,
        [
            "update",
            "101",
            "otro_v2",
            "175",
            "12333",
            "blonde",
            "green",
            "blue",
            "male",
            "2",
        ],
    )
    assert result.exit_code == 0
    print(result.output)


def test_delete(runner):
    result = runner.invoke(cli, ["delete", "101"])
    assert result.exit_code == 0
    print(result.output)
