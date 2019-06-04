# Copy h5 files to binary dir
FILE(GLOB all_h5_files RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} *.h5)
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/${all_h5_files} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
# Copy other files
FILE(COPY SrVO3.pmat SrVO3.struct SrVO3.outputs SrVO3.oubwin SrVO3.ctqmcout SrVO3.symqmc SrVO3.sympar SrVO3.parproj SrIrO3_rot.h5 hk_convert_hamiltonian.hk LaVO3-Pnma_hr.dat LaVO3-Pnma.inp DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# List all tests
set(python_tests wien2k_convert hk_convert w90_convert sumkdft_basic srvo3_Gloc srvo3_transp sigma_from_file blockstructure analyse_block_structure_from_gf analyse_block_structure_from_gf2)
set(doc_tests)
if(${Test_documentation})
    # check if triqs_cthyb is available
    execute_process(
                COMMAND python -c "import triqs_cthyb"
                RESULT_VARIABLE cthyb_status
                OUTPUT_QUIET ERROR_QUIET)
    if(${cthyb_status} EQUAL 0)
		set(doc_tests ${doc_tests} test_SrVO3)
    endif()
    set(all_tests ${all_tests} ${doc_tests})
endif()

set(python_executable python)

if(${TEST_COVERAGE})
    set(python_executable ${PYTHON_COVERAGE} run --append --source "${CMAKE_BINARY_DIR}/python" )
endif()

set(all_tests ${python_tests} ${doc_tests})

foreach(t ${python_tests})
  add_test(NAME ${t} COMMAND ${python_executable} ${CMAKE_CURRENT_SOURCE_DIR}/${t}.py)
endforeach()

foreach(t ${doc_tests})
  add_test(NAME ${t} COMMAND ${python_executable} ${CMAKE_BINARY_DIR}/doc/scripts/${t}.py)
endforeach()

# Set the PythonPath : put the build dir first (in case there is an installed version).
set_property(TEST ${all_tests} PROPERTY ENVIRONMENT PYTHONPATH=${CMAKE_BINARY_DIR}/python:$ENV{PYTHONPATH} )

# VASP converter tests
add_subdirectory(plovasp)
