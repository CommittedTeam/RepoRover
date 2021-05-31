import pytest
from reporover import get_commit_data as cd

@pytest.mark.parametrize(
    "input_message,expected_type",
    [
     ('refactor: rename commit message verification script\n\ncommit message body', "refactor"),
     ('refactor(scope): rename commit message verification script', "refactor"),
     ('refactor commit message verification script', None),
     ('refactor commit message: verification script', None),
    ]
)
def test_get_commit_types(input_message, expected_type):
    """Test the correctness of commit types."""
    commit_type = cd.get_commit_types(input_message)
    assert expected_type == commit_type

@pytest.mark.parametrize(
    "input_list,expected_list",
    [(['.ci/verify-commit-message.py', 'LICENSE', '.gitmessage'], [".py","",""])],
)
def test_parse_for_extension(input_list, expected_list):
    """Test the correctness of file format parsing."""
    parsed_list = cd.parse_for_extension(input_list)
    assert expected_list == parsed_list


@pytest.mark.parametrize(
    "input_list,expected_output",
    [(['.tests/test-commit-message.py', 'LICENSE', '.gitmessage','.scr/commit.py'], ["",".py"])],
)
def test_get_file_extensions(input_list, expected_output):
    """Check that unique file extensions are returned."""
    sorted_formats = cd.get_file_extensions(input_list)
    assert expected_output == sorted_formats


@pytest.mark.parametrize(
    "input_list,expected_output",
    [
        (['.tests/test-commit-message.py', 'LICENSE', '.gitmessage'], 1),
        ([],0)
    ],
)
def test_test_files(input_list, expected_output):
    """Chack that test_files counts test files correctly."""
    count = cd.test_files(input_list)
    assert expected_output == count


@pytest.mark.parametrize(
    "input_list,expected_output",
    [
     ('refactor: rename commit message verification script\n\ncommit message body', "rename commit message verification script\n\ncommit message body"),
     ('refactor(scope): rename commit message verification script', "rename commit message verification script"),
     ('[refactor] rename commit message verification script', 'rename commit message verification script')
    ],
)
def test_get_subject_line(input_list, expected_output):
    """Chack that test_files_ratio gives the ratio correctly."""
    subject = cd.get_subject_line(input_list)
    assert expected_output == subject

@pytest.mark.parametrize(
    "input_tuple,expected_output",
    [
     (("allcontributors[bot]","allcontributors[bot]@users.noreply.github.com"),True),
     (("bagashvilit","bagashvilit@allegheny.edu"),False)
    ],
)
def test_isbot(input_tuple, expected_output):
    """Chack that bots are detected correctly."""
    print(input_tuple)
    boolean = cd.isbot(input_tuple[0],input_tuple[1])
    assert expected_output == boolean