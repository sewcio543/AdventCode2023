CI_COMMIT_MESSAGE="Update problem description."
CI_COMMIT_AUTHOR="Github Actions - Problem Update"

git config --global user.name "$CI_COMMIT_AUTHOR"
git config --global user.email "username@users.noreply.github.com"

if [ -n "$(git status --porcelain)" ]; then
  echo "Update of problem descriptions.";
  git add .
  git commit -m "$CI_COMMIT_MESSAGE"
  git push
else
  echo "No changes detected in problem description markdown.";
fi