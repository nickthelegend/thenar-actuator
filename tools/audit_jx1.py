"""Read pinned JX1 sources through gh, extract factual catalogue comparison.
No hardware access, commands or claims of dynamic robot validation.
"""
from pathlib import Path
import subprocess,json,base64,math
import yaml
ROOT=Path(__file__).resolve().parents[1]
SHA='384de0f801f8a03af6b32420fd2efed343133eb0'
def get(path):
    raw=json.loads(subprocess.check_output(['gh','api',f'repos/nickthelegend/thenar-jx1/contents/{path}?ref={SHA}']))
    return base64.b64decode(raw['content']).decode('utf-8')
catalog=yaml.safe_load(get('actuators/actuator_catalog.yaml'))
jointmap=yaml.safe_load(get('simulation/joint_map.yaml'))
rows=[]
for cls,v in catalog['classes'].items():
    rows.append(dict(actuator_class=cls,count=v['count'],locations=v['joints'],
        selected_peak_Nm=v.get('peak_torque_Nm',v.get('stall_torque_Nm',{})).get('value'),
        selected_rated_Nm=v.get('rated_torque_Nm',{}).get('value')))
assert sum(r['count'] for r in rows)==23
ratio_cases=[]
for ratio in [9,15,20,30,50,82]:
    ratio_cases.append(dict(ratio=ratio,assumed_efficiency=.8,
        motor_torque_for_36Nm=36/(ratio*.8),
        motor_rpm_at_hypothetical_output_6rad_s=6*ratio*60/(2*math.pi),
        holding_arithmetic_only_output_Nm=.55*ratio*.8))
report=dict(source_repo='nickthelegend/thenar-jx1',source_commit=SHA,
    audit_date='2026-10-16',classes=rows,main_actuators=21,neck_servos=2,
    declared_joint_count=jointmap['dof']['total_actuated'],ratio_trade=ratio_cases,
    physical_test_status='NOT_PERFORMED',robot_dynamic_simulation_status='NOT_RUN_WITH_THIS_ACTUATOR',
    jx1_replacement_status='FAIL: torque-speed, geometry and electrical interface not qualified',
    note='Selected actuator capabilities are upstream catalogue values, not new measurements. Ratio calculations use assumed efficiency and hypothetical speed.')
(ROOT/'verification/jx1-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
