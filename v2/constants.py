SECURE_SESSIONID = 'gcdotcom_secure_sessionid'
SESSIONID = 'gcdotcom_sessionid'
SET_COOKIE = 'Set-Cookie'
CSRFTOKEN = 'csrftoken'
CSRFMIDDLEWARETOKEN = 'csrfmiddlewaretoken'
EMAIL = 'email'
PASSWORD = 'password'
REFERER_VAL = 'https://gc.com/login'
LAST_VIEWED = 'last_team_viewed' # goes along with TEAM_ID

BASE_URL = 'https://gc.com'
LOGIN_URI = '/login'
DO_LOGIN_URI = '/do-login'
DO_LOGOUT_URI = '/do-logout'
STATS_URI = '/stats/team' # THIS NEEDS PATH PARAM /{team_id} as well. Get from user input
BATTING_STANDARD = '?stats_requested=%5B%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PA%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22H%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%221B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%222B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%223B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22HR%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22RBI%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22R%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22HBP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22ROE%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22FC%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22CI%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22BB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SO%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AVG%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22OBP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SLG%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22OPS%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%22%2C%22category%22%3A%22offense%22%7D&game_filter=Qualified'
BATTING_PSP = '?stats_requested=%5B%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PA%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PA%2FBB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22BB%2FK%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22C%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SOL%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22CS%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SB%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PIK%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GIDP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GITP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22XBH%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22TB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AB%2FHR%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22BA%2FRISP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SLG%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%22%2C%22category%22%3A%22offense%22%7D&game_filter=Qualified'
BATTING_QABS = '?stats_requested=%5B%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PA%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PS%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PS%2FPA%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%222S%2B3%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%222S%2B3%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%226%2B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%226%2B%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22FLB%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GB%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SHB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SHF%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22LOB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%222OUTRBI%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22HARD%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22QAB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22QAB%25%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22BABIP%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%22%2C%22category%22%3A%22offense%22%7D&game_filter=Qualified'
PITCHING_STANDARD = '?stats_requested=%5B%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22outs%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22GP%3AP%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22GS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22W%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22L%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SV%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SVO%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SV%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22H%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22R%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22ER%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BB%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SO%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22HBP%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22ERA%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22WHIP%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%3AP%22%2C%22category%22%3A%22defense%22%7D&game_filter=Qualified'
PITCHING_COMMAND = '?stats_requested=%5B%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22outs%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BF%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22TS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22S%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22FPS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22FPS%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22FPSO%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22FPSW%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22FPSH%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BB%2FINN%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%220BBINN%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BBS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22LOBB%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22LOBBS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22WP%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%3AP%22%2C%22category%22%3A%22defense%22%7D&game_filter=Qualified'
PITCHING_BATTER = '?stats_requested=%5B%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22outs%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BF%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22AB%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22%23P%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SM%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SM%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SO%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22K%2FG%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22K%2FBF%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22K%2FBB%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22WEAK%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22HARD%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22GB%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22FLY%25%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22GO%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22AO%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22GO%2FAO%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BAA%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22HR%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BABIP%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%3AP%22%2C%22category%22%3A%22defense%22%7D&game_filter=Qualified'
PITCHING_RUNS = '?stats_requested=%5B%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22outs%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22LOB%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22BK%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22PIK%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SB%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22CS%22%7D%2C%7B%22category%22%3A%22defense%22%2C%22key%22%3A%22SB%25%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%3AP%22%2C%22category%22%3A%22defense%22%7D&game_filter=Qualified'