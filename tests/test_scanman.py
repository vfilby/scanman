import logging
import pytest
import os
import tempfile
import shutil

import scanman.scanman

from scanman.scanman import Scanman
from scanman.logpipe import LogPipe


scanman.scanman.configure_logger()


valid_scans = ["scan-1", "scan-2"]
watch_path = "./test-data"
completed_path = "/tmp"
runtime_path = "./runtime"

env = { "INTAKE_DIR": "/tmp/intake", "COMPLETED_DIR": "/tmp/completed" }


temp_directory = tempfile.mkdtemp()
temp_watch_path = os.path.join( temp_directory, "intake" )
temp_completed_path = os.path.join( temp_directory, "completed" )
shutil.copytree( watch_path, temp_watch_path )
os.mkdir( temp_completed_path )
print( "cloned data tmp_dir: '%s'" % temp_directory )


@pytest.fixture()
def scanman_test_data():
    return Scanman( watch_path=watch_path, completed_path=completed_path )

@pytest.fixture()
def scanman_test_data_clone( printer ):
    return Scanman( watch_path=temp_watch_path, completed_path=temp_completed_path )

# @pytest.fixture
# def mock_env_configuration(monkeypatch):
#     for k,v in env.items():
#         monkeypatch.setenv( k, v )


##
## Naming utilities
##
def test_scan_name( scanman_test_data ):
    test_watch_path = scanman_test_data.watch_path
    for scan in valid_scans:
        name = scanman_test_data.get_scan_name( os.path.join( test_watch_path, scan ) )
        assert scan == name

def test_combined_path( scanman_test_data ):
    test_watch_path = scanman_test_data.watch_path
    for scan in valid_scans:
        scan_dir = os.path.join( test_watch_path, scan )
        path = scanman_test_data.get_combined_pdf_path( scan_dir )
        assert path == os.path.join( scan_dir, "%s.combined.pdf" % scan )

def test_output_path( scanman_test_data ):
    test_watch_path = scanman_test_data.watch_path
    test_completed_path = scanman_test_data.completed_path
    for scan in valid_scans:
        scan_dir = os.path.join( test_watch_path, scan )
        path = scanman_test_data.get_output_pdf_path( scan_dir )
        assert path == os.path.join( test_completed_path, "%s.pdf" % scan )

# ##
# ## Getting configuration from ENV
# ##
# def test_env_configuration( mock_env_configuration ):
#
#     assert os.environ.get(watch_path_env) == "/tmp/intake"
#     assert os.environ.get(completed_path_env) == "/tmp/completed"


##
## Manifest validation and use
##
def test_validate_manifest( scanman_test_data ):
    for scan in valid_scans:
        is_valid = scanman_test_data.validate_scan_files( os.path.join( watch_path, scan ) )
        assert is_valid

def test_missing_manifest( scanman_test_data ):
    is_valid = scanman_test_data.validate_scan_files( os.path.join( watch_path, "scan-2-no-manifest" ) )
    assert not is_valid

def test_file_with_bad_hash( scanman_test_data ):
    is_valid = scanman_test_data.validate_scan_files( os.path.join( watch_path, "scan-2-bad-hash" ) )
    assert not is_valid

def test_files_from_manifest( scanman_test_data ):
    files = scanman_test_data._get_files_from_manifest( "./test-data/scan-2" )
    assert len( files ) == 6
    for i in range( len(files) ):
        assert files[i] == "scan-000%d" % (i+1)


##
## pdf processing (these take awhile)
##
@pytest.mark.slow
def test_create_combined_pdf( scanman_test_data_clone ):
    scan_dir = os.path.join( scanman_test_data_clone.watch_path, "scan-1" )
    result = scanman_test_data_clone.process_scan( scan_dir )
    assert result
    logging.debug( "scan_dir: '%s'" % scan_dir )
    logging.debug( "combined: '%s'" % scanman_test_data_clone.get_combined_pdf_path( scan_dir ) )
    assert os.path.isfile( scanman_test_data_clone.get_combined_pdf_path( scan_dir ) )

@pytest.mark.slow
def test_create_searchable_pdf( scanman_test_data_clone ):
    scan_dir = os.path.join( scanman_test_data_clone.watch_path, "scan-1" )
    combined_pdf = scanman_test_data_clone.get_combined_pdf_path( scan_dir )
    output_pdf = scanman_test_data_clone.get_output_pdf_path( scan_dir )
    scan_name = scanman_test_data_clone.get_scan_name( scan_dir )

    result = scanman_test_data_clone.create_searchable_pdf( combined_pdf, output_pdf )

    assert os.path.isfile( os.path.join( temp_directory, "completed", "%s.pdf" % scan_name ) )
