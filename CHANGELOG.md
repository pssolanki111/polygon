# Changelog - `polygon`

All notable changes to the project are documented here.

Version history is sorted from most recent release to the least recent

---

## `v1.2.1` - (2024-08-03)

-  Add Business websocket host as an enum

## `v1.2.0` - (2024-01-30)

-  Add support for all INDEX endpoints. Available as `IndexClient`

## `v1.1.6` - (2024-01-28)

-  Add missing feature - pagination on Technical Indicator endpoints. Thanks `afestekjian` for reporting it.

## `v1.1.4 - v1.1.5` - (2024-01-10)

-  Added `second` aggregate timespan as an enum. Thanks @Slade Wilson for letting me know.

## `v1.1.3` - (2023-11-14)

-  Gracefully handle JSON Parser issues (Thanks @MuradGithub for the contribution)
-  Add `info` log level handler to pagination methods (Thanks @MuradGithub for the contribution)
-  Add `tos1` option symbol format. (Thanks @greko6 for bringing this up as [#16](https://github.com/pssolanki111/polygon/issues/16))

## `v1.1.2` - (2023-09-24)

-  Fixed minor bug: Wrong underlying API call for `get_macd`. [#14](https://github.com/pssolanki111/polygon/issues/14)

## `v1.1.1` - (2023-09-21)

-  `as_of` parameter now supported on option contract endpoint
-  Restructure of requirements file and minor updates to documentation

## `v1.1.0` - (2022-09-13)

-  Added the new technical Indicator endpoints to library. Includes SMA, EMA, RSI and MACD. See docs for more details.

## `v1.0.9` - (2022-07-11)

- Added [Bulk Ticker Details](https://polygon.readthedocs.io/en/latest/bulk_data_download_functions.html#bulk-ticker-details). Thanks to @AlbusFrigoris for the suggestion.
- Bulk download functions get [their own page](https://polygon.readthedocs.io/en/latest/bulk_data_download_functions.html) in the documentation. You may suggest new functions on our [Discord Server](https://discord.gg/jPkARduU6N)
- Forex and crypto documentations are merged into a [single page](https://polygon.readthedocs.io/en/latest/Forex_Crypto.html).
- Added the method `get_dates_between` and added custom timezone support to `normalize_datetime`.
- Other internal changes that you don't care about

---
## `v1.0.8` - (2022-06-25)

- Docs for this version are available [Here](https://polygon.readthedocs.io/en/1.0.8/)
- Removed orjson from REST clients, using `.json()` response method again due to a drop in multicore performance. 
  Thanks to @Baker XBL for the reports.
- The option symbology is UPDATED and BETTER than ever. [Docs](https://polygon.readthedocs.io/en/latest/Options.html#working-with-option-symbols) are re-written. Support for 6 symbol formats added.
- added `force_uppercase_symbols` on both streamers to allow optionally disabling the upper case enforcement
- The option symbology change is not backward compatible. Hence, I've decided to keep the documentation for `v1.0.7` 
  persistent. You can use the **version switch on bottom left of documentation** to navigate between documentation for different versions
- If you were not using option symbology so far, you should not have any issues upgrading. If you were, just update 
  existing code to use new structure (which is very similar so should be very quick to change)
- Added the total downloads badge on GH readme

---
## `v1.0.7` - (2022-06-05)

- Docs for this version are available [Here](https://polygon.readthedocs.io/en/1.0.7/)
- We now have an Official `CHANGELOG`. View it [HERE](https://github.com/pssolanki111/polygon/blob/main/CHANGELOG.md). 
  Thanks to @Baker XBL for the suggestion
- The lib will now use `orjson` if it's installed for all JSON operations. `orjson` is no longer a required 
   dependency for the library. Both `uvloop` and `orjson` are moved to optional extra dependencies. See [here](https://polygon.readthedocs.io/en/latest/Getting-Started.html#installing-polygon) for 
  more info
- An issue with `lt, gt, lte & gte` filters was fixed. Thanks to @Baker XBL for the report & reproducible examples

---
## `1.0.6` - (2022-04-21)

- option contract endpoint added to reference client. view [here](https://polygon.readthedocs.io/en/latest/References.html#get-option-contract)
- All `pagination` methods now accept a `verbose` argument defaulting to False. Setting it to `verbose=True` will print relevant status messages about
  the underlying pagination process. **Useful for people who don't trust me** and want to know what exactly the lib is 
  doing at a certain point in time. 
- Links to official documentation were broken due to a change by polygon.io, which restructured all links. (kinda don't like the new schema lol). 
  That should be fixed. All methods now have correct direct specific links to their official counterparts.
- some internal changes to how the lib handles `timestamp` and `datetimes` and `dates`. To know how to fine tune results, 
  see [relevant docs](https://polygon.readthedocs.io/en/latest/Getting-Started.html#passing-dates-datetime-values-or-timestamps)

---
## `v1.0.5` - (2022-03-04)

- newly released `options quotes` endpoints are now included in the lib. They were released by polygon yesterday I
  believe. Both `http` and `websocket` streaming endpoints are covered
- Some updates to interfacing around `vX/v3` because polygon would deprecate a few older v2 endpoints tomorrow 
  (mar 5th). To maintain backward compatibility, I have tried my best to raise relevant warnings. 
- other internal bug fixes which you don't care about :P

---
## `1.0.2` - (2022-02-06)

- the `better aggregates` functionality is officially released & documented. gets a dedicated section 
  [in the docs](https://polygon.readthedocs.io/en/latest/Getting-Started.html#better-aggregate-bars-function)
  . HUGE thanks to @Baker XBL for the suggestions and helping test it. 
- Other internal changes and fixes which, again, you don't care about :D

---
## `v1.0.1` - (2022-01-29)

- The pagination functionality is officially released and documented 
  [here](https://polygon.readthedocs.io/en/latest/Getting-Started.html#pagination-support)

---
## `1.0.0` - (2022-01-25)

- Marks our **FIRST Production Release**
- the powerful filter options of `lt, lte, gt, gte` (less than, less than or equal to and so on) is patched to work 
  well. Thanks to @Slade Wilson for letting me know about the issue. 
- ThinkOrSwim dot notation parser fixed. thanks to @fatdragon and @Baker XBL  for the inputs. 
- More control over `timeouts` and limits on `httpx pool`. Came across a limitation while helping in @AlbusFrigoris's 
  use case. Suitable for highly concurrent async applications.  

---
## `v0.9.8` - (2022-01-18)

- added the new `stock splits` and `stock dividends` endpoints (V3 of both). deprecated the older ones. 
- `ticker details vx` is now `ticker details v3` (damn it polygon, stop changing paths). all of the above endpoints are 
  no longer experimental.
- added support for `dot notation` for option symbols from `tda` (encountered when exporting any data from ThinkOrSwim 
  or similar tools). thanks to @Slade Wilson for the suggestion
- added a function to detect the option symbol format. recognises polygon standard, tda API and ThinkOrSwim dot 
  notation. thanks to @Baker XBL for the suggestion.

---
## `0.9.6` - (2021-11-16)

- added ALL `options endpoints` (newly released)

---
## `v0.9.5` - (2021-11-07)

- Update the lib based on changes by polygon to endpoints

---
## `0.8.2` - (2021-10-20 )

- Re-did the entire async interface.
- The docs for this version are available [here](https://polygon.readthedocs.io/en/0.8.2/)
- It is highly suggested to upgrade if you're using this version. This was the only version which wasn't backward 
  compatible

---
#### All past releases were meant for initial testings and MUST be upgraded to the latest version.
