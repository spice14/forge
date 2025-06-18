@echo off
SETLOCAL ENABLEEXTENSIONS

:: Root directory
set "ROOT=ForgeTest"

:: Create base structure
mkdir %ROOT%
cd %ROOT%

:: Create subfolders
mkdir forge
mkdir forge\modules
mkdir forge\agents
mkdir forge\prompts
mkdir tests
mkdir tests\fixtures
mkdir examples
mkdir examples\demo-output
mkdir examples\demo-output\tests
mkdir scripts

:: Create files in root
type nul > requirements.txt
type nul > README.md
type nul > LICENSE
type nul > CONTRIBUTING.md
type nul > .env.example

:: Create main files in forge/
echo. > forge\__init__.py
echo. > forge\cli.py
echo. > forge\config.py

:: Modules
echo. > forge\modules\__init__.py
echo. > forge\modules\repo.py
echo. > forge\modules\scan.py
echo. > forge\modules\agent.py
echo. > forge\modules\output.py
echo. > forge\modules\test_runner.py
echo. > forge\modules\utils.py

:: Agents
echo. > forge\agents\__init__.py
echo. > forge\agents\planner.py
echo. > forge\agents\test_writer.py
echo. > forge\agents\refiner.py
echo. > forge\agents\memory.py

:: Prompts
echo. > forge\prompts\base_prompt.txt
echo. > forge\prompts\refinement_prompt.txt
echo. > forge\prompts\coverage_feedback_prompt.txt

:: Tests
echo. > tests\__init__.py
echo. > tests\test_cli.py
echo. > tests\test_repo.py
echo. > tests\test_scan.py
echo. > tests\test_agent.py

:: Scripts
echo. > scripts\run_local.sh
echo. > scripts\setup_env.sh

:: Done
echo.
echo ForgeTest structure created successfully.
cd ..
ENDLOCAL
