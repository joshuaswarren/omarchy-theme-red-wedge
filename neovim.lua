return {
  {
    "echasnovski/mini.base16",
    lazy = false,
    priority = 1000,
    config = function()
      require("mini.base16").setup({
        palette = {
          base00 = "#efe5d0",
          base01 = "#e5dabf",
          base02 = "#ddd2b8",
          base03 = "#8a8272",
          base04 = "#5c554c",
          base05 = "#211c18",
          base06 = "#1a1613",
          base07 = "#100d0b",
          base08 = "#c33d2e",
          base09 = "#b06327",
          base0A = "#c99a2e",
          base0B = "#6d7a4f",
          base0C = "#4f7d76",
          base0D = "#46688c",
          base0E = "#8a4a5e",
          base0F = "#a02f22",
        },
      })
    end,
  },
}
