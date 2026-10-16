from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import JobApplication
from app.schemas import (
    ApplicationStatus,
    JobApplicationCreate,
    JobApplicationRead,
    JobApplicationUpdate,
)


app = FastAPI(
    title="Cloud-Native Application Platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/applications",
    response_model=JobApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: JobApplicationCreate,
    db: Session = Depends(get_db),
):
    application = JobApplication(
        company=payload.company,
        role=payload.role,
        application_date=payload.application_date,
        status=payload.status.value,
        notes=payload.notes,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@app.get(
    "/applications",
    response_model=list[JobApplicationRead],
)
def list_applications(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = (
        select(JobApplication)
        .order_by(JobApplication.id.desc())
        .limit(limit)
    )

    applications = db.scalars(statement).all()

    return applications


@app.get(
    "/applications/{application_id}",
    response_model=JobApplicationRead,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application


@app.patch(
    "/applications/{application_id}",
    response_model=JobApplicationRead,
)
def update_application(
    application_id: int,
    payload: JobApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    non_nullable_fields = {
        "company",
        "role",
        "application_date",
        "status",
    }

    for field, value in updates.items():
        if field in non_nullable_fields and value is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{field} cannot be null",
            )

        if isinstance(value, ApplicationStatus):
            value = value.value

        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


@app.delete(
    "/applications/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
