import pytest
from pytest_mock import MockerFixture

from fython.fame_to_python import fame_to_pandas


def test_fame_to_pandas_no_fame(mocker: MockerFixture) -> None:
    mock_has_fame = mocker.patch("fython.fame_to_python._has_fame", return_value=False)
    with pytest.raises(RuntimeError) as exception:
        fame_to_pandas(["db1", "db2"], "Q", "2023:1", "2023:2", "search-str")
    assert str(exception.value) == "Fame is not found"
    assert mock_has_fame.call_count == 1


def test_fame_to_pandas(mocker: MockerFixture) -> None:
    run_result = ";x\n2020q1;1\n2020q2;1"
    mock_has_fame = mocker.patch("fython.fame_to_python._has_fame", return_value=True)
    mock_run_fame_commands = mocker.patch(
        "fython.fame_to_python._run_fame_commands", return_value=run_result
    )
    result = fame_to_pandas(["db1", "db2"], "Q", "2023:1", "2023:2", "search-str")
    assert len(result) == 2
    assert mock_has_fame.call_count == 1
    assert mock_run_fame_commands.call_count == 1
