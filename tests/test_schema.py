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

from pytest import mark as m

from npgtracking.db.retrieval import get_runs_by_currentstatus


@m.describe("SchemaModel")
class TestSchemaModel(object):
    @m.context("When retrieving run records from tracking DB")
    @m.context("When there are no runs having a current status and manufacturer name")
    @m.it("Empty list is returned")
    def test_schema_no_runs(self, mlwh_session):
        status = "run mirrored"
        manufacturer = "Ultima Genomics"
        tracking_runs = get_runs_by_currentstatus(mlwh_session, status, manufacturer)
        assert len(tracking_runs) == 0

    @m.context("When retrieving run records from tracking DB")
    @m.context(
        "When only one run has the specified current status and manufacturer name"
    )
    @m.it("Metadata of the returned run is correct")
    def test_schema_single_run(self, mlwh_session):
        status = "run in progress"
        manufacturer = "Ultima Genomics"
        tracking_runs = get_runs_by_currentstatus(mlwh_session, status, manufacturer)

        assert len(tracking_runs) == 1
        run = tracking_runs.pop()
        current_run_status = list(
            filter(lambda st: st.iscurrent == 1, run.run_status)
        ).pop()
        assert run.id_run == 50001
        assert run.id_instrument == 130
        assert run.flowcell_id == "424091"
        assert run.folder_name == "424091-20250823_0117"
        assert run.instrument_format.manufacturer.name == manufacturer
        assert current_run_status.run_status_dict.description == status

    @m.context("When retrieving run records from tracking DB")
    @m.context(
        "When there are more runs having the same current status and manufacturer name"
    )
    @m.it("Multiple runs are returned")
    def test_schema_multiple_runs(self, mlwh_session):
        status = "off-tool automation in progress"
        manufacturer = "Ultima Genomics"
        tracking_runs = get_runs_by_currentstatus(mlwh_session, status, manufacturer)

        assert len(tracking_runs) == 2
        for run in tracking_runs:
            run = tracking_runs.pop()
            current_run_status = list(
                filter(lambda st: st.iscurrent == 1, run.run_status)
            ).pop()
            assert run.instrument_format.manufacturer.name == manufacturer
            assert current_run_status.run_status_dict.description == status
