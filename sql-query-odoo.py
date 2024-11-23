start_date = datetime.datetime.now()

olusmayanlar = [1]

for partner in model.search([('id', 'in', olusmayanlar)]):

  if (datetime.datetime.now() - start_date).seconds / 60 >=9:
    break
  sql_query = """ 
            SELECT log.user_id, log.create_date
            FROM auditlog_log_line AS log_line
            JOIN auditlog_log AS log
                ON log_line.log_id = log.id
            WHERE log_line.field_id = 14401
                AND log.model_id = 77
                AND log.res_id = %s
            ORDER BY log_line.create_date DESC
            LIMIT 1;
  """ % partner.id
  env.cr.execute(sql_query)
  response = env.cr.fetchall()

  partner['x_from_cron'] = True
  if response and response[0] and response[0][0]:
    try:
      partner['x_erisim_loglar_ids'] = [(0,0,{'x_related_user':int(response[0][0]), 'x_tarih':response[0][1]})]
    except Exception as e:
      log("Error: %s ,record(%s)" % (str(e),partner.id))