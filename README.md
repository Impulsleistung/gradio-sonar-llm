**Integration and Testing on Local Docker Engine:**

Export the api-key with: `export $(xargs < .env)`

1.  **Build the Docker Image:**

    Open a terminal, navigate to the `perplexity-sonar-app` directory, and run the following command:

    ```bash
    docker build -t perplexity-sonar-app .
    ```

2.  **Run the Docker Container:**

    Run the built image, mapping port 7860 of the container to port 7860 on your host machine:

    ```bash
    docker run -p 7860:7860 --env-file .env perplexity-sonar-app
    ```

    * `--env-file .env`: This loads the environment variables from your `.env` file into the container.
    * `-p 7860:7860`: This maps port 7860 from the container to port 7860 on your host.

3.  **Access the Application:**

    Open your web browser and go to `http://localhost:7860`. You should see the Gradio interface.

4.  **Test the Application:**

    Enter a prompt in the text box and click "Submit." The application will send the prompt to the Perplexity API and display the response.

## The Docmaker

The call goes like `python docmaker_mmd.py > mmd_chart.txt`.
This file cannot exist together with `docmaker_comprehensive.py > document.txt`.