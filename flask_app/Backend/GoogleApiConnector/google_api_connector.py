from googleapiclient import discovery

compute = discovery.build('compute', 'v1')
request = compute.instances().stop(project="sonic-shuttle-322109", zone="europe-west6-a", instance="instance-1")
request.execute()


from google.auth import compute_engine
credentials = compute_engine.Credentials()
print(credentials)