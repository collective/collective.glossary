*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IBasic-title
${title_selector_term} =  input#form-widgets-title
${description_selector} =  textarea#form-widgets-IBasic-description

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to Homepage

    Create Glossary  The Beatles
    Create Term  The Beatles  John
    Create Term  The Beatles  Paul
    Create Term  The Beatles  George
    Create Term  The Beatles  Ringo
    Check Terms  The Beatles  John  Paul  George  Ringo

*** Keywords ***

Click Add Glossary
    Open Add New Menu
    Click Link  css=a#glossary
    Page Should Contain  Add Glossary

Click Add Term
    Open Add New Menu
    Click Link  css=a#term
    Page Should Contain  Add Term

Create Glossary
    [arguments]  ${title}

    Click Add Glossary
    Input Text  css=${title_selector}  ${title}
    Click Button  Save
    Page Should Contain  Item created

Create Term
    [arguments]  ${glossary}  ${title}

    Click Add Term
    Input Text  css=${title_selector_term}  ${title}
    Click Button  Save
    Page Should Contain  Item created

    Click Link  ${glossary}

Check Terms
    [arguments]  ${glossary}  @{terms}

    :FOR  ${term}  IN  @{terms}
    \   Page Should Contain  ${term}
