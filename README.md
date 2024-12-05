## MadMONAI

The AI summarizer for MadMoney by Jim Cramer!

## Demo

![Loading Bar](imgs/webapp2.png)

## Tech Stack

**Client:** React, Tailwind (Daisy UI)

**Server:** Python

## Run Locally

> **⚠️ Warning:** There were no AI API keys in this project. All LLMS were run locally. A **GPU** is **REQUIRED** for running locally.

> To run this project, you will need to add these to .env:
> `MONGO_URI` > `VITE_GOOGLE_CLIENT_ID` > `GOOGLE_SECRET_KEY`

Clone the project

```bash
  git clone https://github.com/ved-patel226/MadMoneyAI.git
```

Go to Frontend directory

```bash
  cd MadMoneyAI/frontend
```

Install react dependencies

```bash
  npm i
```

Go to Backend directory

```bash
  cd .. /backend
```

Install python dependencies

```bash
  pip install -r requirements.txt
```

Go to Frontend directory

```bash
  cd frontend
```

Start Server

```bash
  npm run dev
```
