from CustomExceptions.UserCustomExceptions import (
    UserAlreadyRegister,
    UserValuesNotFound,
    UserInvalidDataUpdate,
    UserDeleteWhitoutSucess,
    UserMemberInvalid
    )

from CustomExceptions.LoginCustomExceptions import (
    UserNotFound,
    UserCredentialsInvalids,
    UserDatasNotSend
)

from CustomExceptions.TeamCustomExceptions import (
    TeamDatasNotSend,
    TeamNotFound,
    BossTeamDoesExist,
    TeamAlreadyExist,
    BossAlreadyGotTeam,
    BossAlreadyInsertTeam
)

from CustomExceptions.OperationsDatabaseExceptions import(
    OperationAggregationFailed
)

from CustomExceptions.ProjectsCustomExceptions import(
    DatasNotSend,
    ProjectAlreadyExist,
    ProjectTypeNotFound,
    UserWithoutPermission,
    DatasInvalidsToChange,
    ProjectNotFound,
    ConflictAboutTheOwner,
    EmailsInvalidToAdd
)