# Contributing to the Repository

## Feature Requests

If you have a new feature you would like to add to the repository, first check if that feature has already been created.
If it hasn't, create an issue with the `enhancement` (or `documentation` if applicable) tag.  It should contain the following:
 * A title containing the name of the feature
 * A brief discription of the feature.  If you want to add a command, include the command's syntax (eg: `foo [bar]`)

Optionally, if you have already completed the next steps before creating an issue, you can put all this in a pull request instead.
 
At this stage, the issue may be taken down if it turns out to be impossible or unnecessary.  If there is enough agreement
on whether the feature is needed, you can put a link to the fork where work will be done
on the feature.  Make sure the branch stays up-to-date with the main source.  Any issues with the feature found during
this stage should be reported to the fork's issue tracker, not here.  You will need to include:
 * Help/documentation on all new commands.  This can be a simple pydoc string at the beginning of the function containing
 a short description on what the command does, and information on any arguments.  Complex docmentation can be on a wiki page,
 but is optional.
 * Tests for any applicable features.  It is reccommended that you write as many test cases as possible to ensure good development
 
 When you feel like the features are ready for release, you may create a pull request referencing the original
 issue.
  * All of the following [checks](https://github.com/FreehandBlock51/OSFA/actions) on the pull request MUST pass:
    * `build (3.8)`
    * `build (3.9)`
    * `build (3.10)`
  * Make sure to put a link to the pull request in the issue.
  * The title of the pull request should provide a list of the features added
  * Any compatability issues or requested changes should be disussed on this pull request and resolved before merging.
Once all requirements have been met and all discussions are closed, you can request one final review from someone who has permissions to merge the pull request, who will decide whether or not to merge it.  If they merge or close the pull request, then the corresponding issue is closed.  Otherwise, they will request changes to be made, and this stage will repeat until the merger makes a final decision.  All stale pull requests will be closed, along with their corresponding issues.

## Versioning

The version of this package is defined as: \
`[release].[patch]`\
where `release` is incremented anytime new features are added, and `patch` is incremented anytime bugs are fixed, but nothing new is added.  Anytime a pull request is merged, one of these should be incremented depending on the changes made.
