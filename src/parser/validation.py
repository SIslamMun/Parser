"""Validation utilities for references and metadata."""

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from .parser import ParsedReference, ReferenceType


@dataclass
class ValidationError:
    """A validation error for a reference."""
    field: str
    message: str
    severity: str = "error"  # "error", "warning", "info"


@dataclass
class ValidationResult:
    """Result of validating a reference."""
    valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationError]

    def __bool__(self) -> bool:
        return self.valid


def validate_reference(ref: ParsedReference) -> ValidationResult:
    """Validate a parsed reference.

    Args:
        ref: Reference to validate

    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []

    # Validate year
    if ref.year:
        try:
            year_int = int(ref.year)
            if not (1900 <= year_int <= 2099):
                errors.append(ValidationError(
                    field="year",
                    message=f"Year {ref.year} is outside valid range (1900-2099)",
                    severity="error"
                ))
            elif year_int > 2030:
                warnings.append(ValidationError(
                    field="year",
                    message=f"Year {ref.year} is in the future",
                    severity="warning"
                ))
        except ValueError:
            errors.append(ValidationError(
                field="year",
                message=f"Year '{ref.year}' is not a valid integer",
                severity="error"
            ))

    # Validate DOI format
    if ref.type == ReferenceType.DOI:
        if not validate_doi(ref.value):
            errors.append(ValidationError(
                field="value",
                message=f"Invalid DOI format: {ref.value}",
                severity="error"
            ))

    # Validate arXiv ID format
    if ref.type == ReferenceType.ARXIV:
        if not validate_arxiv_id(ref.value):
            errors.append(ValidationError(
                field="value",
                message=f"Invalid arXiv ID format: {ref.value}",
                severity="error"
            ))

    # Validate URL
    if ref.url:
        if not validate_url(ref.url):
            errors.append(ValidationError(
                field="url",
                message=f"Invalid or malformed URL: {ref.url}",
                severity="error"
            ))

    # Validate GitHub repo format
    if ref.type == ReferenceType.GITHUB:
        if not validate_github_repo(ref.value):
            errors.append(ValidationError(
                field="value",
                message=f"Invalid GitHub repository format: {ref.value}",
                severity="error"
            ))

    # Check for missing metadata
    if ref.type == ReferenceType.PAPER:
        if not ref.title:
            warnings.append(ValidationError(
                field="title",
                message="Paper reference missing title",
                severity="warning"
            ))
        if not ref.authors:
            warnings.append(ValidationError(
                field="authors",
                message="Paper reference missing authors",
                severity="info"
            ))

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_doi(doi: str) -> bool:
    """Validate DOI format.

    Args:
        doi: DOI string

    Returns:
        True if valid DOI format
    """
    # DOI must start with 10. followed by registrant code (4+ digits)
    # then slash and suffix
    pattern = r'^10\.\d{4,}/[^\s]+$'
    return bool(re.match(pattern, doi))


def validate_arxiv_id(arxiv_id: str) -> bool:
    """Validate arXiv ID format.

    Args:
        arxiv_id: arXiv ID string

    Returns:
        True if valid arXiv ID format
    """
    # New format: YYMM.NNNNN or YYMM.NNNNNvN
    # Old format: archive/YYMMNNN
    new_pattern = r'^\d{4}\.\d{4,5}(v\d+)?$'
    old_pattern = r'^[a-z-]+/\d{7}$'
    return bool(re.match(new_pattern, arxiv_id) or re.match(old_pattern, arxiv_id))


def validate_url(url: str) -> bool:
    """Validate URL format and accessibility.

    Args:
        url: URL string

    Returns:
        True if URL appears valid
    """
    try:
        result = urlparse(url)
        # Must have scheme and netloc at minimum
        if not all([result.scheme, result.netloc]):
            return False
        # Scheme should be http or https
        if result.scheme not in ['http', 'https', 'ftp']:
            return False
        # Check for malformed URLs (missing closing parentheses, etc.)
        # Count parentheses
        open_parens = url.count('(')
        close_parens = url.count(')')
        if open_parens != close_parens:
            return False
        return True
    except Exception:
        return False


def validate_github_repo(repo: str) -> bool:
    """Validate GitHub repository format.

    Args:
        repo: Repository string (owner/repo format)

    Returns:
        True if valid format
    """
    # Must be owner/repo format
    if '/' not in repo:
        return False

    parts = repo.split('/')
    if len(parts) != 2:
        return False

    owner, name = parts
    # Basic validation: alphanumeric, hyphens, underscores
    # Owner and repo name must not be empty
    if not owner or not name:
        return False

    # Check for valid characters
    valid_chars = re.compile(r'^[a-zA-Z0-9_.-]+$')
    if not valid_chars.match(owner) or not valid_chars.match(name):
        return False

    return True


def validate_references(refs: list[ParsedReference], fix: bool = False) -> tuple[list[ParsedReference], list[ValidationResult]]:
    """Validate a list of references.

    Args:
        refs: List of references to validate
        fix: If True, attempt to fix common issues

    Returns:
        Tuple of (validated_refs, validation_results)
    """
    results = []
    validated_refs = []

    for ref in refs:
        result = validate_reference(ref)
        results.append(result)

        if result.valid:
            validated_refs.append(ref)
        elif fix:
            # Attempt to fix common issues
            fixed_ref = _fix_reference(ref, result)
            if fixed_ref:
                # Re-validate
                new_result = validate_reference(fixed_ref)
                if new_result.valid:
                    validated_refs.append(fixed_ref)
                    results[-1] = new_result

    return validated_refs, results


def _fix_reference(ref: ParsedReference, validation_result: ValidationResult) -> ParsedReference | None:
    """Attempt to fix common validation issues.

    Args:
        ref: Reference with validation issues
        validation_result: Validation result

    Returns:
        Fixed reference or None if cannot fix
    """
    from copy import deepcopy
    fixed = deepcopy(ref)

    for error in validation_result.errors:
        if error.field == "url" and error.message.startswith("Invalid or malformed URL"):
            # Try to fix missing closing parenthesis
            if fixed.url and '(' in fixed.url and fixed.url.count('(') > fixed.url.count(')'):
                fixed.url = fixed.url + ')'

    return fixed
