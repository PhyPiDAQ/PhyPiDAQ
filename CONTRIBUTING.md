# Contributing to PhyPiDAQ

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to PhyPiDAQ. These are mostly guidelines, not rules. Use your best
judgment, and feel free to propose changes to this document in a pull request.

## How Can I Contribute?

### Reporting bugs

* **Ensure the bug was not already reported** by searching on GitHub under
  [Issues](https://github.com/PhyPiDAQ/PhyPiDAQ/issues).
* Please be as specific as possible, when you try to report a bug.

### Pull Requests

Please follow these steps to have your contribution considered by the maintainers:

1. Ensure, that you code is working.
2. Write a pull request description, that clearly explains you changes.
3. After you submit your pull request, verify that all status checks are passing.

#### What if the status checks are failing?

If a status check is failing, and you believe that the failure is unrelated to your change, please leave a comment on
the pull request explaining why you believe the failure is unrelated. We will take a look into it and decide on the next
steps.

### Code linting

We are using Continuous-Integration (CI) to check our `Python` code. This includes linting the code using the `ruff`
package. To install it, simply run the following command in your terminal: 

```shell
pip3 install -r requirements_dev.txt
```

If the installation succeeded, you can use `ruff` to test your code locally by executing the following command:

```shell
ruff check <filename>
ruff format --check <filename>
```

## Contributors

Here is a list of all contributors sorted alphabetically by lastname

* Moritz Aupperle
* Alexander Becker
* Dominik Braig
* Raphael Grau
* Alexander Kaschta
* Achim Pelster
* Günter Quast
* M. Wong
