import pytest
from unittest.mock import MagicMock
from datetime import date, datetime, timedelta
from repositories.contact_repository import ContactRepository, Contact
from schemas.contacts import ContactCreate, ContactUpdate

@pytest.fixture
def mock_db_session(mocker):
    """Fixture to provide a mock database session."""
    return mocker.MagicMock()

@pytest.fixture
def contact_repository(mock_db_session):
    """Fixture to provide a ContactRepository instance with a mock session."""
    repo = ContactRepository()
    repo.db = mock_db_session
    return repo

def test_get_all_by_user(contact_repository, mock_db_session):
    """Test fetching all contacts for a specific user."""
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Contact(id=1, user_id=1, first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="1234567890", birthday=date.today(), additional_data="Test data"),
        Contact(id=2, user_id=1, first_name="Jane", last_name="Doe", email="jane.doe@example.com", phone_number="9876543210", birthday=date.today(), additional_data="More data")
    ]
    contact_repository.db = mock_db_session
    contacts = contact_repository.get_all_by_user(1)
    assert len(contacts) == 2
    assert contacts[0].first_name == "John"
    assert contacts[1].email == "jane.doe@example.com"

def test_get_by_id_and_user(contact_repository, mock_db_session):
    """Test fetching a specific contact by its ID and user ID."""
    mock_db_session.query.return_value.filter.return_value.first.return_value = Contact(id=1, user_id=1, first_name="John", last_name="Doe")
    contact_repository.db = mock_db_session
    contact = contact_repository.get_by_id_and_user(1, 1)
    assert contact.first_name == "John"
    assert contact.user_id == 1

def test_create_for_user(contact_repository, mock_db_session):
    """Test creating a new contact."""
    contact_data = ContactCreate(first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="1234567890", birthday=date.today(), additional_data="Test data")
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()
    contact_repository.db = mock_db_session

    contact = contact_repository.create_for_user(contact_data, 1)
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert contact.first_name == "John"

def test_update_for_user(contact_repository, mock_db_session):
    """Test updating a contact with optional fields."""
    contact_data = ContactUpdate(
        first_name="John Updated",
        additional_data="Updated additional notes"
    )

    mock_contact = MagicMock(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="1234567890",
        birthday=date(1990, 1, 1),
        additional_data="Old notes"
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_contact
    contact_repository.db = mock_db_session

    def mock_setattr(instance, name, value):
        instance.__dict__[name] = value

    updated_contact = contact_repository.update_for_user(1, contact_data, 1)

    assert mock_contact.first_name == "John Updated"
    assert mock_contact.additional_data == "Updated additional notes"
    assert mock_contact.last_name == "Doe"
    assert mock_contact.email == "john.doe@example.com"
    assert mock_contact.phone_number == "1234567890"
    assert mock_contact.birthday == date(1990, 1, 1)

def test_delete_for_user(contact_repository, mock_db_session):
    """Test deleting a contact."""
    mock_contact = MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_contact
    mock_db_session.delete = MagicMock()
    mock_db_session.commit = MagicMock()
    contact_repository.db = mock_db_session

    deleted_contact = contact_repository.delete_for_user(1, 1)
    mock_db_session.delete.assert_called_once_with(mock_contact)
    mock_db_session.commit.assert_called_once()
    assert deleted_contact == mock_contact

def test_search_by_user(contact_repository, mock_db_session):
    """Test searching contacts for a user."""
    mock_db_session.query.return_value.filter.return_value.filter.return_value.all.return_value = [
        Contact(id=1, user_id=1, first_name="John", last_name="Doe"),
    ]
    contact_repository.db = mock_db_session

    results = contact_repository.search_by_user(1, first_name="John")
    assert len(results) == 1
    assert results[0].first_name == "John"

def test_get_upcoming_birthdays_by_user(contact_repository, mock_db_session):
    """Test fetching upcoming birthdays."""
    today = datetime.today()
    upcoming_contact = Contact(
        id=1,
        user_id=1,
        first_name="John",
        last_name="Doe",
        birthday=(today + timedelta(days=3)).date(),
    )
    mock_db_session.query.return_value.filter.return_value.all.return_value = [upcoming_contact]
    contact_repository.db = mock_db_session

    results = contact_repository.get_upcoming_birthdays_by_user(1)
    assert len(results) == 1
    assert results[0].birthday == (today + timedelta(days=3)).date()
