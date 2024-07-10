#@STCGoal Wrap the Feature preparation done in these sessions.  As result: we have a file for an input POV in the JGTPY_DATA_FULL/mlf/$i_$t.csv
##@STCGoal It contains columns feature ready for the model.
""" # TO ADJUST....
  'price_peak_above', 'price_peak_bellow', 'ao_peak_above',
       'ao_peak_bellow', 'mfi_sq', 'mfi_green', 'mfi_fade', 'mfi_fake',
       'mfi_sig', 'mfi_str', 'mfi_str_M1', 'zcol_M1', 'ao_M1', 'mfi_str_W1',
       'zcol_W1', 'ao_W1'
"""
##@STCGoal It can be a source for the making of MX Data.

from jgtml import mfihelper2 as mfihelper, mxconstants as mxc, mxhelper as mxhelper,realityhelper,zonehelper

def create_mlf_data__STUB(i,
                          t,
                          use_full=True,
                    add_mfis_lag_feature=True,
                    add_zone_lag_feature=True,
                    add_ao_above_bellow_peaks_lag_feature=True,
                    add_ao_lag_feature=True,
                    add_obs_sig_normal_mouth_is_open=False,
                    add_obs_sig_is_out_of_normal_mouth=False,
                    add_obs_sig_is_in_big_teeth=False,
                    add_obs_sig_big_mouth_is_open_and_in_big_lips=False,
                    add_obs_sig_big_mouth_is_open_and_in_big_teeth=False,
                    add_obs_sig_is_in_tide_teeth=False,
                    add_obs_sig_tide_mouth_is_open_and_in_tide_lips=False,
                    add_obs_sig_tide_mouth_is_open_and_in_tide_teeth=False,
                    ):
  """
  Wrap all the creation we've been doing in the prototyping sessions. (2407) - See: pto_240706_patterning_helper.ipynb,pto_240706_patterning_helper_C02.ipynb,pto_240706_patterning_helper_C03.ipynb,pto_240706_patterning_helper_C04.ipynb,pto_240706_patterning_helper_C04b.ipynb,pto_240706__validation_240709.ipynb, $jgtml/samples/jgtml_obsds_240515_SIGNALS.result.csv
  
  Parameters:
  i: str - the instrument
  t: str - the timeframe
  use_full: bool - use the full data or not
  add_mfis_lag_feature: bool - add the mfi lag feature or not
  add_zone_lag_feature: bool - add the zone lag feature or not
  add_ao_above_bellow_peaks_lag_feature: bool - add the ao above bellow peaks lag feature or not
  add_ao_lag_feature: bool - add the ao lag feature or not (CURRENTLY IMPLEMENTED in the add_mfis_lag_feature)
  add_obs_sig_normal_mouth_is_open: bool - FDB Buy/Sell Flag Signal when Normal Mouth is Open (The normal alligator mouth is Open)
  add_obs_sig_is_in_big_teeth: bool - Signal In the Big Alligator Teeth
  add_obs_sig_big_mouth_is_open_and_in_big_lips: bool - Big Alligator Mouth is Open and FDB Buy Signal is in the Big Alligator Lips
  add_obs_sig_big_mouth_is_open_and_in_big_teeth: bool - Big Alligator Mouth is Open and FDB Buy Signal is in the Big Alligator Teeth
  add_obs_sig_is_in_tide_teeth: bool - Signal In the Tide Alligator Teeth
  add_obs_sig_tide_mouth_is_open_and_in_tide_lips: bool - Tide Alligator Mouth is Open and FDB Buy Signal is in the Tide Alligator Lips
  add_obs_sig_tide_mouth_is_open_and_in_tide_teeth: bool - Tide Alligator Mouth is Open and FDB Buy Signal is in the Tide Alligator Teeth
  
  """
  raise NotImplementedError('Not implemented yet.  See: pto_240706_patterning_helper.ipynb,pto_240706_patterning_helper_C02.ipynb,pto_240706_patterning_helper_C03.ipynb,pto_240706_patterning_helper_C04.ipynb,pto_240706_patterning_helper_C04b.ipynb,pto_240706__validation_240709.ipynb')
  pass

  