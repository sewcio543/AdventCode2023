CI_COMMIT_MESSAGE="New problem update."
CI_COMMIT_AUTHOR="Github Actions - Problem Update"

git config --global user.name "$CI_COMMIT_AUTHOR"
git config --global user.email "username@users.noreply.github.com"

if [ -n "$(git status --porcelain)" ]; then
  echo "Pulling changes from remote.";
  git pull
  echo "New problem update.";
  git add .
  git commit -m "$CI_COMMIT_MESSAGE"
  git push
else
  echo "No changes detected.";
fi
