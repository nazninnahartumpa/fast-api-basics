import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueUpdate, IssueOut, IssueStatus
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """Retrieve a list of all issues."""

    issues = load_data()
    return issues


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
async def create_issue(payload: IssueCreate):
    """Create a new issue."""

    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "status": IssueStatus.open,
        "priority": payload.priority,
    }

    issues.append(new_issue)
    save_data(issues)
    return new_issue


@router.get("/{issue_id}", response_model=IssueOut)
async def get_issue(issue_id: str):
    """Retrieve a specific issue by its ID."""

    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)

    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    return issue


@router.put("/{issue_id}", response_model=IssueOut)
async def update_issue(issue_id: str, payload: IssueUpdate):
    """Update an existing issue."""

    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)

    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    if payload.title is not None:
        issue["title"] = payload.title
    if payload.description is not None:
        issue["description"] = payload.description
    if payload.status is not None:
        issue["status"] = payload.status
    if payload.priority is not None:
        issue["priority"] = payload.priority

    save_data(issues)
    return issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(issue_id: str):
    """Delete an existing issue."""

    issues = load_data()
    issue = next((issue for issue in issues if issue["id"] == issue_id), None)

    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    issues.remove(issue)
    save_data(issues)
