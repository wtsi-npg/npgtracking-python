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
    """
    Returns a list of npgtracking.db.schema::Run objects for runs with
    current status as given by the status_description argument and performed
    on an instrument by a manufacturer given by the manufacturer argument.
    It does not validate either the status description or the manufacturer name.
    Examples:
        status_description: "run in progress"
        manufacturer_name: "Ultima Genomics"

    Args:
        session (sqlalchemy.orm.Session): Session object
        status_description (str): One of the run statuses, should exist
            in the run_status_dict table
        manufacturer_name (str): Manufacturer name as defined in the manufacturer table

    Returns:
        list[Run]: All runs with a specific current status and manufacturer name
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
