# git-rescope — Terms of Service, License & Legal Notices

Version 1.0 | Effective Date: 2026-06-07

---

## 1. Acceptance of Terms

By installing, copying, or using git-rescope ("the Software"), you ("User") agree
to be bound by these Terms of Service ("Terms"). If you do not agree, do not use
the Software.

---

## 2. License

The Software is distributed under the MIT License:

    Copyright (c) 2026 git-rescope contributors

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

---

## 3. No Warranty / Disclaimer

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. THE AUTHORS
EXPRESSLY DISCLAIM ALL WARRANTIES, WHETHER EXPRESS, IMPLIED, STATUTORY, OR
OTHERWISE, INCLUDING WITHOUT LIMITATION: WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, TITLE, AND NON-INFRINGEMENT.

**GIT OPERATIONS ARE DESTRUCTIVE BY NATURE. THE SOFTWARE MODIFIES YOUR GIT
WORKING TREE, CREATES AND POPS STASHES, AND CHECKS OUT BRANCHES. THERE IS AN
INHERENT RISK OF DATA LOSS. YOU ACCEPT FULL RESPONSIBILITY FOR ANY LOSS OF CODE,
UNCOMMITTED WORK, OR DATA ARISING FROM THE USE OF THIS SOFTWARE.**

---

## 4. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL THE AUTHORS,
CONTRIBUTORS, OR MAINTAINERS BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING BUT NOT LIMITED TO: LOSS OF DATA,
LOSS OF PROFITS, LOSS OF BUSINESS, OR LOSS OF GOODWILL) ARISING OUT OF OR IN
CONNECTION WITH THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

---

## 5. Data Storage & Privacy

git-rescope stores the following data **locally on your machine only**:

- Snapshot metadata: branch names, file paths, timestamps, descriptions.
- A HMAC signature file for tamper detection.
- A machine-bound key (`machine.key`) used solely for local integrity verification.
- An audit log of CLI invocations (can be disabled in `config.json`).

**git-rescope does NOT transmit any data over the network.** All data remains
on your local filesystem under `~/.config/git-rescope/`. You may delete this
directory at any time to remove all stored data.

---

## 6. Security Responsibilities

The User is responsible for:

- Keeping `~/.config/git-rescope/` secure (permissions are set to 700 on Unix).
- Not sharing `machine.key` or `storage.json` with untrusted parties.
- Ensuring that snapshot descriptions do not contain sensitive information.
- Reviewing restored patches before applying them to critical branches.

The Software employs the following security controls:
- HMAC-SHA256 integrity verification on `storage.json`.
- Input validation and path-traversal prevention on all user inputs.
- Append-only audit logging of all CLI invocations.
- Sensitive key material is zeroed from memory on drop (via the `zeroize` crate).
- Zero shell-injection surface: Git operations use native libgit2 bindings.

---

## 7. Acceptable Use

You agree NOT to use this Software to:

- Circumvent security controls in any organisation's Git infrastructure.
- Store credentials, passwords, API keys, or other secrets in snapshot descriptions.
- Interfere with other users' repositories without authorisation.
- Violate any applicable law or regulation.

---

## 8. Third-Party Dependencies

This software includes third-party open-source components. Their licenses are
available via `cargo license` or in the `Cargo.lock` file. Key dependencies:

| Crate                | License        |
|----------------------|----------------|
| git2 / libgit2       | GPL-2 / LGPL-2 |
| ratatui              | MIT            |
| clap                 | MIT / Apache-2 |
| serde / serde_json   | MIT / Apache-2 |
| uuid                 | MIT / Apache-2 |
| chrono               | MIT / Apache-2 |
| sha2 / hmac          | MIT / Apache-2 |
| zeroize              | MIT / Apache-2 |
| dirs                 | MIT            |

---

## 9. Changes to Terms

The maintainers reserve the right to update these Terms at any time. Continued
use of the Software after a new version is released constitutes acceptance of
the updated Terms.

---

## 10. Governing Law

These Terms shall be governed by and construed in accordance with applicable
open-source software norms. Disputes shall be resolved in the jurisdiction of
the principal maintainer.

---

*Run `grs terms` to display this document at any time.*
