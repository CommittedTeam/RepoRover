import pytest

from reporover import get_convention

@pytest.mark.parametrize(
    "input_commits,expected_conventions",
    [
      ("test(matchers): add support for toHaveClass in tests", "angular"),
      ("refactor(WebWorker): Unify WebWorker naming\n\nCloses #3205","angular"),
      ("style(WebWorker): Unify WebWorker naming\n\nCloses #3205","angular"),
      ("feat: upgrade ts2dart to 0.7.1", "angular"),
      (":memo: Fix license", "atom"),
      (":memo: Add a screenshot\n\n", "atom"),
      (":fire: init", "atom"),
      ("[BUGFIX beta] Guard 'meta' and move readonly error to prototype.", "ember"),
      ("[DOC beta] Add docs for get helper", "ember"),
      ("Chore: Don't expose jQuery.access", "eslint"),
      ("Breaking: don't use deprecated argument in test declaration", "eslint"),
      ("Update: Added as-needed option to arrow-parens (fixes #3277)", "eslint"),
      ("[[FEAT]] Add Window constructor to browser vars", "jshint"),
      ("[[FEAT]] Add pending to Jasmine's globals", "jshint"),
      ("refactor test functions", "undefined"),
      ("Add new feature: detect conventions","undefined"),
      ("Update readme","undefined")
    ]
)
def test_match(input_commits, expected_conventions):
    """Check that match returns correct convention."""
    conventions = get_convention.match(input_commits)
    assert conventions == expected_conventions
