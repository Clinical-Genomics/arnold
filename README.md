# Arnold  [![Coverage Status](https://coveralls.io/repos/github/Clinical-Genomics/arnold/badge.svg?branch=master)](https://coveralls.io/github/Clinical-Genomics/arnold?branch=master)

Arnold is a  REST-API and mongodb database with two collections - `sample` and `step`. Currently, soring lims-data only. 

Data is continuously pushed into the database from lims steps via [cg_lims](https://github.com/Clinical-Genomics/cg_lims) commands, using the arnold REST-API.

[Read more about the lims data that is being pushed to Arnold.](https://github.com/Clinical-Genomics/cg_lims#about-arnold)


## Usage

### Development

Clone and install:

```bash
git clone https://github.com/Clinical-Genomics/arnold
cd arnold
pip install -r requirements.txt -e .
```

Create a .env file with the variables `DB_NAME` and `DB_URI`

```
DB_URI= 'mongodb://localhost:<port>'
DB_NAME= 'arnold'
```

Given you have a MongoDB server listening on the `port` specified in .env, the arnold rest API can be run from commandline

```bash
arnold serve --reload
```

### Docker image

Arnold can also run as a container. The image is available [on Docker Hub][docker-hub] or can be build using the 
Dockerfile provided in this repository.

To build a new image from the Dockerfile use the commands: `docker build -t arnold .`

To run the image use the following command: `docker run --name arnold `

To remove the container, type: `docker rm arnold`

## Release model
Arnold is using github flow release model as described in our development manual.


### Steps to make a new release:

1) Get you PR approved.
2) Append the version bump to PR title. Eg. __Update README__ becomes __Update Readme (patch)__
3) Select __squash and merge__
4) Write a change log comment.
5) Merge.

	
### Deploying to staging

Opening pull requests in Arnold repository will enable a Github Action to build containers and publish to 
[arnold-stage dockerhub](https://hub.docker.com/repository/docker/clinicalgenomics/arnold-stage) with each commit.

Two tags will be published: one with the name of the branch and another tagged "latest".


Steps to test current branch on staging:

`ssh firstname.lastname@cg-vm1.scilifelab.se`

`sudo -iu hiseq.clinical`

`ssh localhost`
  
If you made changes to internal app : `systemctl --user restart arnold.target` 

Your branch should be deployed to staging at https://arnold-stage.scilifelab.se 

If for some reason you cannot access the application at given address, check status of the container: `systemctl --user status arnoldApp.service`

### Deploying to production

Use `update-arnold.sh` script to update production both on Hasta and CGVS. 
**Please follow the development guide and `servers` repo when doing so. It is also important to keep those involved informed.**


[cg_lims]: https://github.com/Clinical-Genomics/cg_lims
[WisecondorX]: https://github.com/CenterForMedicalGeneticsGhent/WisecondorX
[docker-hub]: https://hub.docker.com/repository/docker/clinicalgenomics/arnold