import pytest

pytestmark = pytest.mark.asyncio(loop_scope="package")
print("I am executing the package Module")
