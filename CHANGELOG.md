# Changelog

<!--next-version-placeholder-->

## v1.2.0 (2022-12-05)
### Feature
* **deploy:** Add initial docker deployment ([`f7695d0`](https://github.com/Kitware/VERACore/commit/f7695d06fe7b1fa16abbc9640773fdf2f6480533))

## v1.1.1 (2022-11-25)
### Fix
* **data:** Allow data to be specified by env variable ([`15da0b4`](https://github.com/Kitware/VERACore/commit/15da0b41068e2907c8e56bef7c68b93fd4c66eb5))

## v1.1.0 (2022-10-07)
### Feature
* **table view:** Add new table view ([`2f13063`](https://github.com/Kitware/VERACore/commit/2f13063d2fdbd91d8cff18c686b0ba5e55e35d6e))
* **volume_view:** Add camera reset button ([`8ed4484`](https://github.com/Kitware/VERACore/commit/8ed4484f6bfd7ade90363d4262c744f64e8e6c5e))
* **selected_line:** Plot selected lines in plots ([`05ea68f`](https://github.com/Kitware/VERACore/commit/05ea68fc5652a32591bd521080fc68825477cda7))
* **volume_view:** Add a volume viewer ([`e280852`](https://github.com/Kitware/VERACore/commit/e280852180f098c38ed363c997b09dfa5b42cd8a))
* **pin_volumes:** Add ability to show pin volumes ([`20d267c`](https://github.com/Kitware/VERACore/commit/20d267cd982da274106eafdbc69ef96a22c2e8b5))
* **core_view:** Add selection ([`4ed5eed`](https://github.com/Kitware/VERACore/commit/4ed5eedf68a86ee0873b38116960181d51c3bf1f))
* **axial_plot:** Added axial plot ([`be52c68`](https://github.com/Kitware/VERACore/commit/be52c6840997871f07201a9df2be59da7cc0734e))
* **assembly_view:** Add assembly view ([`acfb576`](https://github.com/Kitware/VERACore/commit/acfb5769786f322f177125431ff7fd612dc22f76))
* **coreview:** Add core view ([`46d2732`](https://github.com/Kitware/VERACore/commit/46d273200c47ee8567516000f7f24bd07cfd463c))
* **Axial View:** Add axial view and many updates ([`ba843d6`](https://github.com/Kitware/VERACore/commit/ba843d6802359fb55c48d9573ed579a82539ed05))
* **ui:** Add power over time plots with plotly ([`661c25a`](https://github.com/Kitware/VERACore/commit/661c25ace4e91b8fbdcc2bddd5a3578c714739b3))
* **VeraOutFile:** Add VeraOutFile class ([`f14e871`](https://github.com/Kitware/VERACore/commit/f14e871c08f4d3a79239d82b9480dbac150fd091))

### Fix
* **README.rst:** Add `--data <path>` to instructions ([`4f6edb1`](https://github.com/Kitware/VERACore/commit/4f6edb19e8f15801f7bbf10f9068e48d4b2009f3))
* **README.rst:** Fix hyperlink for long description ([`df920b5`](https://github.com/Kitware/VERACore/commit/df920b58fd8776e2bc85406253fadb94854b8e4e))
* **MANIFEST.in:** Add license and select js files ([`ffe0c71`](https://github.com/Kitware/VERACore/commit/ffe0c71d2d19a1853be9b792255f99e640b6a7e7))
* **y axial view:** Fix selected index ([`63e5371`](https://github.com/Kitware/VERACore/commit/63e5371d6d34975ddd1c342556232fe01a323396))
* **double updates:** Only update once after view selections ([`408b64e`](https://github.com/Kitware/VERACore/commit/408b64ece4e6b70ea21b62bd0f39488e059c43e1))
* **tests:** Update import name in pytest ([`612b86b`](https://github.com/Kitware/VERACore/commit/612b86bd88769b25528e36e25a69ff0ade7afdb7))
* **volume:** Small viewer edit ([`5cbcaa2`](https://github.com/Kitware/VERACore/commit/5cbcaa2b7656a1da1c8ddcf58285ae7d7c7162fe))
* **assets:** Add assets to MANIFEST.in ([`26e398f`](https://github.com/Kitware/VERACore/commit/26e398fc3fa445c744fe1bc9a90e9c56c3c845f1))
* **y_axial:** Fix y axial view ([`62e837b`](https://github.com/Kitware/VERACore/commit/62e837b76368c65a96bda2050329ba359b6690ad))
* **color:** Add color map editor ([`ddaf5c8`](https://github.com/Kitware/VERACore/commit/ddaf5c85384d9d36f6eecbd54d7721c2cb2222ee))
* **color_range:** Update color range on array change ([`24ca422`](https://github.com/Kitware/VERACore/commit/24ca422913256a9cd8f5e2d41bc52845142ec8c1))
* **logo:** Add neams logo ([`899d307`](https://github.com/Kitware/VERACore/commit/899d3071b6172576083ca3640e91b55e6f8eb1ee))
* **UI:** Better layout ([`910c656`](https://github.com/Kitware/VERACore/commit/910c6569bb40efd724e76c98bdb7e5e6b928f2f1))
* **ui:** Solve selection ([`7e4810d`](https://github.com/Kitware/VERACore/commit/7e4810d42c5d93026efea6a44819400fe393f225))
* **colormap:** Fix colormap range to match veraview ([`90a3dc0`](https://github.com/Kitware/VERACore/commit/90a3dc02a025ea63bdaa2c23948dc0aa3f4a0341))
* **colormap:** Fix the range to match previous ([`7e79b7b`](https://github.com/Kitware/VERACore/commit/7e79b7b040e0287d5a5e40f72f0c64cd71a966e0))
* **axial_view:** Change default layer to 24 ([`d5d9592`](https://github.com/Kitware/VERACore/commit/d5d95925fb61b793b5a27e9ae621326d0a3617a2))
* **sliders:** Slider range should be one less ([`b132064`](https://github.com/Kitware/VERACore/commit/b13206468d0d1228163afdfc656435e32fc52d16))
* **AxialView:** Use new widget ([`50f17fc`](https://github.com/Kitware/VERACore/commit/50f17fc8cc8768b0c1d3c035c360a87235555fc4))
* **ui:** Update widgets ([`619c007`](https://github.com/Kitware/VERACore/commit/619c0070881364270679e2f57060817eac39b278))
* **core_view:** Clean up core view generation code ([`1e169fc`](https://github.com/Kitware/VERACore/commit/1e169fcb2d023ad4aee80cfb310f179aa7b335b8))
* **core_view:** Remove axes swapping ([`0b02d65`](https://github.com/Kitware/VERACore/commit/0b02d658f225a1a6bd1676a94f1e97154d4af5fa))
* **CoreView:** Add better view but it will need some fix ([`5f6a963`](https://github.com/Kitware/VERACore/commit/5f6a963bd0f21269325c18d90a9ed8afc57b41d3))
* **AssemblyVue:** Replace with custom vera widget ([`664f812`](https://github.com/Kitware/VERACore/commit/664f81235abb93f9aee0c167e186e58c97d98355))
* **layout:** Make layout similar to veraview ([`835815d`](https://github.com/Kitware/VERACore/commit/835815d6645f618d64e6e02f6e1e8eb7cb01a0f8))
* **resizing:** Fix matplotlib views to resize correctly ([`dbb3f49`](https://github.com/Kitware/VERACore/commit/dbb3f49c0689f89750ab8c3a1007f1e6ad1276a2))
* **matplotlib:** Handle dynamic size ([`1ffdc94`](https://github.com/Kitware/VERACore/commit/1ffdc947ac4054077840ecdfa546ac5fa1ad4fab))
* **ColorBar:** Add color bar ([`af76f88`](https://github.com/Kitware/VERACore/commit/af76f883779297d7abada711050d71eff224c428))
* **layout:** Better grid layout handling ([`3bade39`](https://github.com/Kitware/VERACore/commit/3bade39b24a594b4622fb45103c944380a0d4147))
