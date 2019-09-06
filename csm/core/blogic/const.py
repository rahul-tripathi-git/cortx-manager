# Commands
CSM_SETUP_CMD = "csm_setup"
CSM_SETUP_ACTIONS = ['init']
SUPPORT_BUNDLE = 'support_bundle'
EMAIL_CONFIGURATION = 'email'
ALERTS_COMMAND = 'alerts'
ALERTS_CLI_HEADERS = {'id': 'Alert Id',
                      'health': 'Health',
                      'description': 'Description',
                      'severity': 'Severity',
                      'state': 'State',
                      'acknowledge': 'Acknowledged',
                      'resolved': 'Resolved'}
# CSM Agent Port
CSM_AGENT_PORT = 8082

# Initalization
HA_INIT = '/var/csm/ha_initialized'

# File names
SUMMARY_FILE = 'summary.txt'

# Cluster states
STATE_UP = 'up'
STATE_DOWN = 'down'
STATE_DEGRADED = 'degraded'

# ERROR CODES
SUPPORT_BUNDLE_NOT_FOUND = 1000
OS_PERMISSION_DENIED = 2000

# File Collector
BUNDLE_FILE = 'files.tgz'

# Poll check internal
RESPONSE_CHECK_INTERVAL = 1

# Index
CSM_GLOBAL_INDEX = 'CSM'
INVENTORY_INDEX = 'INVENTORY'
COMPONENTS_INDEX = 'COMPONENTS'

# AMQP Consumer Tag
CONSUMER_TAG = 'AMQP_CONSUMER'

# Cluster Inventory Related
INVENTORY_FILE = '/etc/csm/cluster.conf'
KEY_COMPONENTS = 'sw_components'
ADMIN_USER = 'admin_user'
KEY_NODES = 'nodes'
TYPE_CMU = 'CMU'
TYPE_SSU = 'SSU'
TYPE_S3_SERVER = 'S3_SERVER'

# Config
CSM_CONF = '/etc/csm/csm.conf'
CSM_CLUSTER_CONF = '/etc/csm/cluster.conf'
COMPONENTS_CONF = '/etc/csm/components.yaml'
SUPPORT_BUNDLE_ROOT='SUPPORT_BUNDLE_ROOT'
DEFAULT_SUPPORT_BUNDLE_ROOT='/opt/seagate/bundle'
SSH_TIMEOUT = 'SSH_TIMEOUT'
DEFAULT_SSH_TIMEOUT = 5
USER = 'user'
DEFAULT_USER = 'admin'

# Non root user
NON_ROOT_USER='csm'
NON_ROOT_USER_PASS='csm'

# CSM Alert Related
CSM_ALERT_CMD = 'cmd'
GOOD_ALERT = ['insertion', 'fault_resolved']
BAD_ALERT = ['missing', 'fault']
ALERT_ID = 'id'
ALERT_TYPE = 'type'
ALERT_UUID = 'alert_uuid'
ALERT_ENCLOSURE_ID = 'enclosure_id'
ALERT_MODULE_NAME = 'module_name'
ALERT_RESOLVED = 'resolved'
ALERT_ACKNOWLEDGED = 'acknowledged'
ALERT_SEVERITY = 'severity'
ALERT_RESOURCE_TYPE = 'resource_type'
ALERT_MODULE_TYPE = 'module_type'
ALERT_UPDATED_TIME = 'updated_time'
ALERT_CREATED_TIME = 'created_time'
ALERT_INT_DEFAULT = -1
ALERT_TRUE = 1
ALERT_FALSE = 0
ALERT_SENSOR_TYPE = 'sensor_response_type'
ALERT_MESSAGE = 'message'

# CSM Schema Path
CSM_HW_SCHEMA = '/opt/seagate/csm/schema/csm_hw_alert.json'
ALERT_MAPPING_TABLE = '/opt/seagate/csm/schema/alert_mapping_table.json'
