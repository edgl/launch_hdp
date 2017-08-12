
echo "Posting the blueprint"
echo curl -H \"X-Requested-By: ambari\" -X POST -d @blueprint.json -u admin:admin $1:8080/api/v1/blueprints/mycluster
curl -H "X-Requested-By: ambari" -X POST -d @blueprint.json -u admin:admin $1:8080/api/v1/blueprints/mycluster

sleep 3

echo "Posting the template"
echo curl -H \"X-Requested-By: ambari\" -X POST -d @blueprint-template.json -u admin:admin $1:8080/api/v1/clusters/mycluster
curl -H "X-Requested-By: ambari" -X POST -d @blueprint-template.json -u admin:admin $1:8080/api/v1/clusters/mycluster

