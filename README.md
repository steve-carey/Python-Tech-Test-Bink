Python Developer technical challenge for Bink

Arguments:
    * -q1 = This will results in the answers to q1.
    * -q2 = This will results in the answers to q2.
    * -q3 = This will results in the answers to q3.
    * -q4 = This will results in the answers to q4.

Use Case:
    # Returning all answers:
        python .\python_developer_test.py -q1 -q2 -q3 -q4

    # Return a single answer example:
        python .\python_developer_test.py -q1

Unittest Use Case:
    # Run all tests:
        python test_python_developer_test.py
    
    # Run a single test:
        python test_python_developer_test.py TestDeveloperTest.<test_name>
        E.g.
        python test_python_developer_test.py TestDeveloperTest.test_csv_file_exists
