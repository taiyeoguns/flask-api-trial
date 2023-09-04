import logging
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.exc import SQLAlchemyError

from app.models import User

logger = logging.getLogger(__name__)


def validate_user(
    token: str,
    required_scopes: Optional[List[str]],
) -> Union[Dict[str, Any], None]:
    """Validate API user.

    Args:
        token (str): API key
        required_scopes (Optional[List[str]]): Scopes

    Returns:
        Union[Dict[str, Any], None]: User or None
    """
    try:
        user = User.query.filter_by(api_key=token).first()
    except SQLAlchemyError as err:
        logger.exception(err)
        return None

    return None if user is None else {"uid": user}
