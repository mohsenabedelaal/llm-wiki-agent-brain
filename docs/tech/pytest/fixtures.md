# pytest — Fixtures and Test Execution

Canonical: https://docs.pytest.org/en/stable/how-to/fixtures.html

pytest provides modular, reusable fixtures and assert introspection for building readable, scalable test suites.

## Defining and Requesting Fixtures

Test functions request fixtures by declaring arguments matching fixture names:

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_sample(sample_data):
    assert sample_data["key"] == "value"
```

## Fixture Scopes and Reusability

Fixtures are created when requested and destroyed based on `scope`:
- `function` (default): Destroyed at test end.
- `class`: Destroyed during teardown of last test in class.
- `module`: Destroyed during teardown of last test in module.
- `package`: Destroyed during teardown of package.
- `session`: Destroyed at the end of the test session.

```python
@pytest.fixture(scope="module")
def shared_resource():
    resource = create_resource()
    yield resource
    resource.cleanup()
```

## Teardown with Yield Fixtures

Use `yield` fixtures to execute cleanup logic reliably after tests finish:

```python
@pytest.fixture
def managed_resource():
    res = setup_resource()
    yield res
    res.teardown()
```

## Autouse Fixtures and Parametrization

```python
# Autouse fixture runs for all tests in scope without explicit request
@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")

# Parametrized fixtures execute dependent tests for each parameter
@pytest.fixture(params=["sqlite", "postgres"])
def db_type(request):
    return request.param
```

## Repo Review Guidelines

- Tests reside in `tests/` and use standard `pytest` discovery.
- Use `monkeypatch` and `tmp_path` fixtures rather than modifying global state or disk directly.
- Keep unit tests fast, deterministic, and isolated: mock network calls and Gemini API interactions.
