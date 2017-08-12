
aws ec2 run-instances --cli-input-json file://ec2-template.json --count=$EC2_NUM_INSTANCES --tag-specifications "ResourceType=instance,Tags=[{Key=\"Business Unit\",Value=\"${EC2_TAG_BUSINESS_UNIT}\"},{Key=\"Service\",Value=\"${EC2_TAG_SERVICE}\"}, {Key=Product,Value=\"${EC2_TAG_PRODUCT}\"}, {Key=Owner,Value=\"${EC2_TAG_OWNER}\"},{Key=\"End Date\",Value=\"${EC2_TAG_END_DATE}\"}]"
