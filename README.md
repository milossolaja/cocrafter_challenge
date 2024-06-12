# <img src="./frontend/public/favicon.png" height="22pt"> CoCrafter Code Challenge v2

## Requirements 🧗🏽

You are responsible for building a mini web app to make the life of construction companies easier. For simplicity, we
have already provided you with a prototypical frontend. You only need to implement the backend.
Construction companies need to store all their legal documents (e.g. insurance documents). In order for that, they need
a file system that allows them to create folders to store files in them. In each folder they want to be able to store
0 - N files and 0 - N subfolders. Files can have any type (png, pdf, excel,..).

The challenge can be split into the following two parts:

1. **Provide implementations for the endpoints used in ./frontend/src/api.ts**. For details, e.g., return types, please
   refer to the code:
    - `GET /api/v2/folders` - Returns the entire folder hierarchy as a tree, including files. Please refer to the
      appendix for an example response.
    - `POST /api/v2/folders/` - Creates a new folder within the folder identified by the parentId parameter provided in
      the body.
    - `PATCH /api/v2/folders/:id` - Updates the name of the folder with the given id.
    - `DELETE /api/v2/folders/:id` - Deletes the folder with the given id.
    - `GET /api/v2/documents/:id` - Directly returns the file content of the document with the given id. (The file
      should directly be downloaded when accessing this endpoint)
    - `POST /api/v2/documents` - Uploads a new file to the folder identified by the parentId parameter provided in the
      body.
    - `PATCH /api/v2/documents/:id` - Updates the name of the file with the given id.
    - `DELETE /api/v2/documents/:id` - Deletes the file with the given id.

   **Additional information**: You may change the endpoints if needed, as long as no functionality is lost. This should
   not be necessary, nor is it expected though. If you do choose to change anything, make sure to adjust the frontend
   accordingly.

2. **Containerize your application using Docker**. Feel free to modify the docker-compose.yml file as needed. Please
   also provide us with necessary secrets and environment variables. We will not deduct points for unsafe storage of
   these. (Though please use common sense and do not send us sensitive secrets).

   **Additional Information:**
    - The frontend expects the backend to be reachable at http://localhost:8000. (You may also choose a different port,
      but it is your responsibility to adjust the rest of the code accordingly.)
    - We have provided you with a Postgres database and a local S3 mock. Please use these. You can find the connection
      details in the `docker-compose.yml` file.
        - Tip: You can connect with the local S3 API by configuring the `AWS_ENDPOINT_URL` of the chosen S3
          SDK ([reference](https://docs.aws.amazon.com/sdkref/latest/guide/feature-ss-endpoints.html)). You will have to
          configure the SDK to use path-style
          addressing ([reference](https://github.com/adobe/S3Mock?tab=readme-ov-file#path-style-vs-domain-style-access)).
          The S3 instance already has a bucket named `cocrafter-dev` for you to use. See the appendix for an example.
3. ➕ **Bonus Task**:
   - You might have noticed that one component in the frontend is still trying to reach the legacy backend under `/api/v1/ping` using the
same host as the new backend. The legacy backend is provided as a service in the `docker-compose` file. Find a way for the frontend to reach the backend
whilst **addressing the same host** (and port) as your newly implemented backend.
    - **Important Note**: As the title suggests, this is a bonus task meaning that you do not have to complete it in order to proceed to next interview stage.


## Tech Stack 📚

- You are free to use any programming language, framework, and libraries you like.
- You are free to use any external tools (Stack Overflow, ChatGPT, ...)
- You may *not* be aided by another person directly

## Deliverables 📦

Please send the following to `annabell@cocrafter.com`:

- Link to the **private GitHub project**:
    - We should be able to run the mini app by simply running `docker-compose up` (**note**: we will not spend much time
      trying to make your project run - it will count as failed submission!)
    - Code should run without errors & function as expected
    - Clean code (**note**: please structure and comment the project like if it was a real project that you collaborate
      on with multiple developers)
- Add a **README** that explains
    - How long it took you to solve this
    - How did you approach the problem
    - What was the most difficult part & how did you solve it
    - What would you have done differently/ added it this feature would be shipped into production

## Next Steps 🔜

- We will review your final product & code (e.g. based on how you approached the problem...)
- Tech interview call
    - Discuss your deliverable in detail → explain your solution in depth, answer additional questions..
    - More (general) questions session to test your technical knowledge

## Appendix

### Example return from `GET /folders`

```json
{
  "id": "root",
  "name": "Root",
  "children": [
    {
      "id": "folder-1",
      "name": "Folder 1",
      "children": [
        {
          "id": "folder-1-1",
          "name": "Folder 1.1",
          "children": [
            {
              "id": "folder-1-1-1",
              "name": "Folder 1.1.1",
              "children": [],
              "documents": []
            }
          ],
          "documents": [
            {
              "id": "document-4",
              "name": "Document 4"
            }
          ]
        },
        {
          "id": "folder-1-2",
          "name": "Folder 1.2",
          "children": [],
          "documents": []
        }
      ],
      "documents": [
        {
          "id": "document-1",
          "name": "Document 1"
        },
        {
          "id": "document-2",
          "name": "Document 2"
        }
      ]
    },
    {
      "id": "folder-2",
      "name": "Folder 2",
      "children": [],
      "documents": []
    }
  ],
  "documents": [
    {
      "id": "document-3",
      "name": "Document 3"
    }
  ]
}
```

### Example setup of S3 client (JS SDK v3)

(You will have to use an appropriate endpoint, this is just an example.
Any credentials should should be accepted by the S3 mock.)

```typescript
new S3Client({
  endpoint: 'http://localhost:8001',
  region: 'eu-central-1',
  forcePathStyle: true,
  credentials: {
    accessKeyId: 'ACCESS_KEY_ID',
    secretAccessKey: 'ACCESS_KEY_SECRET',
  },
});
```
