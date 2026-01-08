# -*- coding: utf-8 -*-
#
# Copyright © 2025 Genome Research Ltd. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import select
from sqlalchemy.orm import Session

from npgtracking.db.schema import (
    InstrumentFormat,
    Manufacturer,
    Run,
    RunStatus,
    RunStatusDict,
)


def get_runs_by_currentstatus(
    session: Session, status_description: str, manufacturer_name: str
) -> list[Run]:
    """Retrieves run records from the database.

    Retrieves runs with the current status as given by the status_description
    argument, which is performed on an instrument by the manufacturer with the
    name given by the manufacturer_name argument.

    No validation of either the status description or the manufacturer name
    is performed.

    Args:
      session :
        Database session.
      status_description :
        One of the run statuses, should exist in the 'run_status_dict' database
        table.
      manufacturer_name :
        Manufacturer name as defined in the 'manufacturer' database table.

    Returns:
    -------
      A list of runs with a specific current status, which are performed on
      an instrument by a particular manufacturer.

      An empty list is returned if no run satisfies the given criteria.
    """
    query = (
        session.query(Run)
        .join(RunStatus)
        .join(RunStatusDict)
        .join(InstrumentFormat)
        .join(Manufacturer)
    ).filter(
        RunStatusDict.description == status_description,
        RunStatus.iscurrent == 1,
        Manufacturer.name == manufacturer_name,
    )
    return query.all()


def get_run_by_id(
    session: Session,
    batch_id: str | None = None,
    flowcell_id: str | None = None,
    id_run: int | None = None,
) -> Run | None:
    """
    Get a Run by its IDs. Either id_run alone, or batch_id and flowcell_id together

    Args:
      session :
        Database session
      ---
      batch_id :
        The batch ID from DNA pipelines - must be combined with flowcell_id below
      flowcell_id :
        The ID of the flowcell used in the run - must be combined with batch_id
      ---
      id_run :
        NPG Tracking run ID - sufficient on its own

    Returns:
    -------
      npgtracking.db.schema.Run or None
    """

    statement = select(Run)

    if id_run:
        statement = statement.where(Run.id_run == id_run)
    elif batch_id and flowcell_id:
        statement = statement.where(Run.batch_id == batch_id).where(
            Run.flowcell_id == flowcell_id
        )
    else:
        raise ValueError("Can't get one run without an argument")
    result = session.execute(statement).scalar_one_or_none()
    return result
