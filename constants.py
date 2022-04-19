DATABASE_NAME = 'nowgg_developer'

TOKEN_VALIDITY = 24 * 60
COOKIE_VALIDITY = 24 * 60
AWS_SIGNED_URL_VALIDITY = 60 * 60


class Collections:
    USER_ACCOUNT_COLLECTION = "UserAccount"
    COMPANY_COLLECTION = "Company"
    APP_COLLECTION = "App"
    SUBMISSION_COLLECTION = "AppSubmission"
    PROPERTIES_COLLECTION = "Properties"


class AccountType:
    CUSTOMER = "customer"
    SALES_REP = "sales_rep"


class Hosts:
    UI_PROD_HOST = "https://studio.now.gg"
    UI_UAT_HOST = "https://studio-uat.testngg.net"
    UI_QA_HOST = "https://studio-qa.testngg.net"
    UI_QA_1_HOST = "https://studio-qa-1.testngg.net"
    UI_DEV_HOST = "https://studio-dev.testngg.net"
    UI_DEV_1_HOST = "https://studio-dev-1.testngg.net"

    UI_PROD_ADMIN_HOST = "https://admin-studio.now.gg"
    UI_DEV_ADMIN_HOST = "https://admin-studio-dev.testngg.net"
    UI_QA_ADMIN_HOST = "https://admin-studio-qa.testngg.net"
    UI_QA1_ADMIN_HOST = "https://admin-studio-qa-1.testngg.net"
    UI_UAT_ADMIN_HOST = "https://admin-studio-uat.testngg.net"

    API_DEV_HOST = "https://api-studio-dev.testngg.net"
    API_DEV_1_HOST = "https://api-studio-dev1.testngg.net"
    API_QA_HOST = "https://api-studio-qa.testngg.net"
    API_QA_1_HOST = "https://api-studio-qa1.testngg.net"
    API_UAT_HOST = "https://api-studio-uat.testngg.net"
    API_PROD_HOST = "https://api-studio.now.gg"


class Environments:
    DEV = 'dev'
    QA = 'qa'
    QA1 = 'qa1'
    UAT = 'uat'
    PROD = 'prod'


class Origins:
    DEV_ORIGINS = []
    QA_ORIGINS = ['https://studio-qa.testngg.net', 'https://studio-qa-1.testngg.net',
                  'https://admin-studio-qa.testngg.net', 'https://admin-studio-qa-1.testngg.net']
    UAT_ORIGINS = ['https://studio-uat.testngg.net', 'https://admin-studio-uat.testngg.net']
    PROD_ORIGINS = ['https://studiov2.now.gg', 'https://studiov1.now.gg', 'https://studio.now.gg',
                    'https://admin-studio.now.gg']


class Projects:
    DEV_PROJECT = "engg-developer-now-gg"
    QA_PROJECT = "qa-developer-now-gg"
    UAT_PROJECT = "uat-developer-now-gg"
    PROD_PROJECT = "prod-developer-now-gg"


class UserStatus:
    PENDING = 'pending'
    APPROVED = 'approved'


class RegistrationStatus:
    PENDING = 'pending'
    APPROVED = 'approved'


class UserAccountStatus:
    DISABLED = 'disabled'
    ACTIVE = 'active'


class AppStatus:
    DISABLED = 'disabled'
    ACTIVE = 'active'


class CompanyStatus:
    DISABLED = 'disabled'
    ACTIVE = 'active'


class SubmissionStates:
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_TESTING = "under_testing"
    READY_FOR_PUBLISHING = "ready_for_publishing"
    PUBLISHED = "published"
    MARKED_FOR_UNPUBLISHING = "marked_for_unpublishing"
    UNPUBLISHED = "unpublished"
    ARCHIVED = "archived"


class IAP:
    class Hosts:
        PROD = "https://cloud-api.bluestacks.cn"
        DEV = "https://cloud-test-api.bluestacks.cn"

    class AppEndPoints:
        GET_APP_LIST = "/v2/sellers/app/getListData"
        ADD_APP = "/v2/sellers/app/insertDo"
        GET_RSA = "/v2/sellers/app/appTokenInfo"
        UPDATE = "/v2/sellers/app/updateDo"

    class SellerEndPoints:
        GET_ALL_SELLERS = '/v1/sellers/listAll'
        REGISTER_SELLER = "/v2/sellers/registerSeller"
        LIST_WHITELISTED_EMAILS = "/v2/sellers/sandboxWhiteList/getListData"
        ADD_EMAIL_TO_WHITELIST = "/v2/sellers/sandboxWhiteList/insertDo"
        REMOVE_WHITELISTED_EMAIL = "/v2/sellers/sandboxWhiteList/delDo"
        ORDERS_LIST_DATA = "/v2/sellers/order/getListDataAll"

    class TemplateEndPoints:
        LIST = "/v2/sellers/priceTemplate/getListData"
        LIST_ALL = "/v2/sellers/priceTemplate/getAllListData"
        GET = "/v2/sellers/priceTemplate/getExtendListData"
        ADD = "/v2/sellers/priceTemplate/insertDo"
        UPDATE = "/v2/sellers/priceTemplate/updateDo"
        UPDATE_PRICES = "/v2/sellers/priceTemplate/updateExtendDo"

    class ProductEndPoints:
        LIST = "/v2/sellers/goods/getListData"
        GET = "/v2/sellers/goods/info"
        ADD = "/v2/sellers/goods/insertDo"
        UPDATE = "/v2/sellers/goods/updateDo"

    class OrderEndPoints:
        LIST = "/v2/sellers/order/getListData"
        GET = "/v2/sellers/order/details"

    class OrderRefundEndPoints:
        LIST = "/v2/sellers/orderRefund/getListData"
        GET = "/v2/sellers/orderRefund/details"
        APPROVE = "/v2/sellers/orderRefund/sellerAgreeDo"
        REJECT = "/v2/sellers/orderRefund/sellerCancelDo"

    class RevenueEndpoints:
        LIST = "/v2/sellers/statisticData/listData"
        LIST_ALL = "/v2/statistic/getStaticData"
        LIST_USER_LTV = "/v2/sellers/statisticData/listDataLtv"
        LIST_COUNTRY = "/v2/statistic/getStaticCountrySelectList"
        LIST_RECENT_DAYS = "/v2/statistic/getStaticLastDaysData"


class SubmissionType:
    FULL = "full"
    METADATA_CHANGE = "metadata_change"


class AppAssetsSource:
    GOOGLE_PLAY_STORE = "google_play_store"
    MANUAL = "manual"


class APKSource:
    LINK = "web_url"
    GOOGLE_PLAY_LINK = "google_play_link"
    UPLOAD_FILE = "upload_file"


class Email:
    class TemplateIds:
        REGISTRATION_CONFIRMATION = "d-48521497c4284c3dafb0cbdf3f07f314"
        STATE_CHANGE_SUBMITTED = "d-ecc3e212968547b4aca943213ccadd25"
        STATE_CHANGE_PUBLISHED = "d-c420db9025564fde8eb533239c93c9ca"
        STATE_CHANGE_UNPUBLISHED = "d-c03494eb21364c77b455c2c5d704694f"
        STATE_CHANGE_INTERNAL = "d-c378a58573154bc696db8559b355480f"

    class Metadata:
        FROM = "no-reply@now.gg"
        NAME = "Now Studio"
        DEV_SUPPORT = "dev-support@now.gg"
        CAMPAIGN_OPS = 'campaign-ops@now.gg'
        CLOUD_PLAYER = "cloudplayer-qa@bluestacks.com"
        DEV_SUPPORT_TESTING = "dev-support-testing@now.gg"
        QA_EMAIL_LIST = ['meenakshi@bluestacks.com', 'puru.aggarwal@bluestacks.com', 'kaushik.shiyani@bluestacks.com']
        DEVELOPERS_EMAIL_LIST = ['pranshu.gupta@bluestacks.com', 'harshit.agarwal@bluestacks.com']
        DEV_LEADS_EMAIL_LIST = ['ankit@bluestacks.com', 'sakshi@bluestacks.com']


class Stats:
    class ProjectIds:
        STAGING = "staging-now-gg"
        PROD = "prod-now-gg"

    class Datasets:
        ANALYTICS_STAGING = "analytics_258707392"
        ANALYTICS_PROD = "analytics_258749578"


class AppTiers:
    FREE = "free"
    ECONOMY = "economy"
    BUSINESS = "business"
    PREMIUM = "premium"


class EnvType:
    PRODUCTION = 'production'
    STAGING = 'staging'


class ModelChoices:
    APP_TIERS = (AppTiers.FREE, AppTiers.ECONOMY, AppTiers.BUSINESS, AppTiers.PREMIUM)
    REGISTRATION_STATUS_CHOICES = (RegistrationStatus.PENDING, RegistrationStatus.APPROVED)


class PubSub:
    class BQ:
        TOPIC_ID = "bq-insert"


class MiscStats:
    DATASET = 'Miscellaneous'

    class Tables:
        TERMS_ACCEPTED_STATS = "TermsAcceptedStats"
        LOGIN_STATS = "LoginStats"


class AuditStats:
    DATASET = "Audit"

    class Tables:
        SUBMISSION_UPDATE_STATS = "SubmissionUpdateStats"
        APP_UPDATE_STATS = "AppUpdateStats"
        COMPANY_UPDATE_STATS = "CompanyUpdateStats"
        USER_UPDATE_STATS = "UserUpdateStats"

    class EventType:
        ADD = "add"
        UPDATE = "update"
        DELETE = "delete"
        LOGIN = "login"
        TERM_ACCEPTED = "terms_accepted"

    class ActionUserType:
        ADMIN = "admin"
        DEVELOPER = "developer"
        SCRIPT = "script"


class NowggApi:
    GET_ALL_APPS = 'https://now.gg/api/apps/v1/list'


class ErrorMessageStrings:
    OLD_OR_NEW_STATE_REQUIRED = 'Either old or new state required'
    TOKEN_NOT_VALID = 'Token is not valid.'
    TOKEN_MISSING = 'Token is missing.'
    TOKEN_EXPIRED = 'Token expired.'
    OBJECT_CANNOT_BE_SAVED = 'Object cannot be saved.'
    BAD_REQUEST = 'Bad request.'
    AUTHORIZATION_FAILED = 'Authorization failed.'
    USER_DETAILS_NOT_FOUND = 'User details not found.'
    TRANSITION_NOT_ALLOWED = 'Transition not allowed from {} to {}'
    ERROR_WHILE_SENDING_EMAIL = 'Error while sending email - {}'
    MIGRATION_ERROR = 'Migration Errors'


class EmailStrings:
    NOW_STUDIO_MIGRATION = 'Now Studio Migration'


class ApiEndpoints:
    MIGRATE_EXISTING_DEVELOPERS = '/v1/admin/migrate_existing_developers'


class DateFormat:
    Y_M_D = '%Y-%m-%d'
    MONGO = '$date'


class TableHeadings:
    SERIAL_NO = 'S_no.'
    COMPANY_ID = 'Company ID'
    EMAIL = 'Email'
    COMPANY_NAME = 'Company Name'
    COUNTRY = 'Country'
    NAME = 'Name'
    APP_DEVELOPER = 'App Developer'
    APP_PKG = 'App Package Name'
    PLAY_PAGE_URL = 'Play-page Url'
    PUBLISHER_SUBDOMAIN = 'Publisher Subdomain'
    APP_ID = 'App Id'


class UserAccountTypes:
    ADMIN = 'admin'
    DEVELOPER = 'developer'


class OrderEnvironmentTypes:
    RELEASE = 'release'
    SANDBOX = 'sandbox'
