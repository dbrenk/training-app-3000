@echo off
SET CONTAINER_NAME=training-app-container
SET IMAGE_NAME=training-app

REM Check if the container exists
docker ps -a -q -f name=%CONTAINER_NAME% > tmp.txt
set /p CONTAINER_ID=<tmp.txt
del tmp.txt

IF NOT "%CONTAINER_ID%"=="" (
    echo Stopping and removing existing container...
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
)

REM Build the Docker image
echo Building Docker image...
docker build -t %IMAGE_NAME% .

REM Run the container
echo Running new container...
docker run -d -p 5000:5000 --env-file .env --name %CONTAINER_NAME% %IMAGE_NAME%

echo Container is running at http://localhost:5000
pause
